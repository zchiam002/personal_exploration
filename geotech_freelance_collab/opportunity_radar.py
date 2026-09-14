#!/usr/bin/env python3
"""Opportunity radar for a geotechnical freelancer (offshore, nearshore and onshore).

Pulls industry news feeds, scores each item against a keyword profile and
prints a ranked digest. Standard library only: run it from cron or by hand.

    python3 opportunity_radar.py            # last 14 days, top 25
    python3 opportunity_radar.py --days 30 --top 50
    python3 opportunity_radar.py --json > digest.json

A hit is a *trigger*: a contract award, campaign start, vessel mobilisation
or rig move that implies someone now needs a client rep, a leg-penetration
assessment, a driveability check or a report reviewer. The follow-up is a
short, specific outreach message to the company named in the item.
"""
import argparse
import email.utils
import json
import re
import sys
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta, timezone

FEEDS = {
    "offshore-energy.biz": "https://www.offshore-energy.biz/feed/",
    "OE Digital": "https://www.oedigital.com/news/latest?format=feed",
    "Ground Engineering": "https://www.geplus.co.uk/feed/",
    "Hydro International": "https://www.hydro-international.com/rss/news.xml",
    "Windpower NL": "https://windpowernl.com/feed/",
    "Rigzone": "https://www.rigzone.com/news/rss/rigzone_latest.aspx",
    "Baird Maritime": "https://www.bairdmaritime.com/stories.rss",
    # onshore construction, tunnelling and solar
    "New Civil Engineer": "https://www.newcivilengineer.com/feed/",
    "Tunnelling Journal": "https://www.tunnellingjournal.com/feed/",
    "PV-Tech": "https://www.pv-tech.org/feed/",
}

# CORE terms describe the work itself. An item must hit at least one of them
# to be reported at all; everything else only adds weight.
CORE = {
    r"geotechnical|geotechnics": 5,
    r"site investigation|soil investigation|ground investigation|soil survey|geotechnical survey": 5,
    r"\bcpt\b|cone penetration|borehole|drilling campaign|soil sampling|seabed sampl": 4,
    r"jack-?up|spudcan|leg penetration|site[- ]specific assessment|\bssa\b": 6,
    r"pile (capacity|driv|install)|driveability|drivability|monopile|piling": 4,
    r"mudmat|subsea structure|conductor setting": 3,
    r"client rep|client representative|third[- ]party (review|qc)|marine warranty": 4,
    # onshore and nearshore
    r"ground improvement|soil improvement|vibro|deep cement mixing|\bdcm\b|prefabricated vertical drain|surcharge": 4,
    r"slope (stabili|failure|assessment)|landslide|debris flow|rockfall": 4,
    r"tunnel|\btbm\b|shaft|deep excavation|diaphragm wall|retaining wall|earth retaining": 3,
    r"soil (testing|laboratory|lab)|laboratory testing|triaxial|oedometer|consolidation test|iso[/ ]?iec 17025": 4,
    r"instrumentation|settlement monitoring|inclinometer|piezometer|pile load test|\bpda\b|static load test": 4,
    r"foundation (design|failure|works)|bored pile|driven pile|jacked pile|micro ?pile": 3,
}
# TRIGGERS say that money has just moved: someone now needs people.
TRIGGERS = {
    r"\bawarded\b|\bcontract\b|\bsecures?\b|\bwins?\b|\bappointed\b|\btender\b|mobilis|mobiliz|\bcampaign\b": 3,
    r"rig move|rig relocat|\bjackups?\b|rig contract|day ?rates?": 3,
    r"decommission|plug and abandon|\bp&a\b|well abandon": 3,
    r"carbon capture|\bccs\b|carbon storage": 3,
    r"cable route|interconnector|subsea cable|export cable": 2,
    r"reclamation|polder|nearshore|coastal protection|port expansion|jetty|breakwater": 3,
    r"data cent(re|er)|hyperscale|campus": 2,
    r"floating solar|floating pv|\bfpv\b|solar farm|large[- ]scale solar|\blss\d?\b": 2,
    r"\bmrt\b|rail link|airport|terminal 5|expressway|metro": 2,
    r"dispute|arbitration|expert witness|forensic|collapse|sinkhole": 3,
}
# GEOGRAPHY he can reach on 14 days' notice, weighted by how likely he is hired there.
GEOGRAPHY = {
    r"singapore|malaysia|indonesia|vietnam|thailand|brunei|philippines|sarawak|sabah|johor|penang|batam|nusantara": 4,
    r"taiwan|japan|korea|australia|india|middle east|saudi|qatar|\buae\b|abu dhabi": 2,
}
# Named buyers and contractors in his reachable market.
NAMES = {
    r"petronas|\bhelms\b|asian geos|fugro|geoquip|gardline|benthic|\begs\b|horizon geo": 3,
    r"\bcip\b|copenhagen infrastructure|ørsted|orsted|corio|\bjera\b|\bwpd\b|vena energy": 2,
    r"allseas|heerema|sapura|velesto|\bborr\b|valaris|shelf drilling|noble corp|seadrill": 2,
    r"\bhdb\b|\blta\b|\bpub\b|\bjtc\b|\bura\b|\bbca\b|\bmpa\b|changi airport group|\bcag\b": 3,
    r"penta-ocean|koh brothers|samsung c&t|hyundai e&c|gammon|woh hup|china communications|\bccc\b|boskalis|van oord|jan de nul|\bdeme\b": 2,
    r"\btnb\b|masdar|cypark|sunview|gentari|\bpln\b|petrovietnam|\bevn\b": 2,
}
NEGATIVE = [r"\bsolar\b", r"electrolyser", r"battery storage", r"onshore wind", r"\bnaval\b", r"warship"]


def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (radar)"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.read()


def parse(xml_bytes, source):
    root = ET.fromstring(xml_bytes)
    ns = {"atom": "http://www.w3.org/2005/Atom", "content": "http://purl.org/rss/1.0/modules/content/"}
    items = []
    for it in root.iter("item"):  # RSS 2.0
        title = (it.findtext("title") or "").strip()
        link = (it.findtext("link") or "").strip()
        desc = re.sub(r"<[^>]+>", " ", it.findtext("description") or "")
        date = it.findtext("pubDate") or ""
        items.append((source, title, link, desc[:1200], date))
    for it in root.iter("{http://www.w3.org/2005/Atom}entry"):  # Atom
        title = (it.findtext("atom:title", namespaces=ns) or "").strip()
        link_el = it.find("atom:link", ns)
        link = link_el.get("href") if link_el is not None else ""
        desc = re.sub(r"<[^>]+>", " ", it.findtext("atom:summary", namespaces=ns) or "")
        date = it.findtext("atom:updated", namespaces=ns) or ""
        items.append((source, title, link, desc, date))
    return items


def parse_date(s):
    try:
        return email.utils.parsedate_to_datetime(s)
    except Exception:
        pass
    try:
        return datetime.fromisoformat(s.replace("Z", "+00:00"))
    except Exception:
        return None


def score(text):
    t = text.lower()
    core = [(pat, w) for pat, w in CORE.items() if re.search(pat, t)]
    if not core:
        return 0, []
    s, hits = 0, []
    for group in (CORE, TRIGGERS, GEOGRAPHY, NAMES):
        for pat, w in group.items():
            if re.search(pat, t):
                s += w
                hits.append(re.sub(r"\\b|\(|\)|\?", "", pat.split("|")[0]))
    for pat in NEGATIVE:
        if re.search(pat, t):
            s -= 4
    return s, hits


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--days", type=int, default=14)
    ap.add_argument("--top", type=int, default=25)
    ap.add_argument("--min-score", type=int, default=8)
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    cutoff = datetime.now(timezone.utc) - timedelta(days=a.days)

    rows, errors = [], []
    for name, url in FEEDS.items():
        try:
            for src, title, link, body, date in parse(fetch(url), name):
                d = parse_date(date)
                if d and d.tzinfo is None:
                    d = d.replace(tzinfo=timezone.utc)
                if d and d < cutoff:
                    continue
                s, hits = score(f"{title} {body}")
                if s >= a.min_score:
                    rows.append({"score": s, "source": src, "title": title, "link": link,
                                 "date": d.date().isoformat() if d else "", "hits": hits})
        except Exception as e:  # keep going on a single dead feed
            errors.append(f"{name}: {e}")

    rows.sort(key=lambda r: (-r["score"], r["date"]), reverse=False)
    rows = rows[: a.top]
    if a.json:
        json.dump({"items": rows, "errors": errors}, sys.stdout, indent=2)
        return
    print(f"Opportunity radar — last {a.days} days, {len(rows)} hits (min score {a.min_score})\n")
    for r in rows:
        print(f"[{r['score']:>2}] {r['date']}  {r['title']}")
        print(f"      {r['source']} · {r['link']}")
        print(f"      triggers: {', '.join(r['hits'][:8])}\n")
    if errors:
        print("Feed errors:\n  " + "\n  ".join(errors))


if __name__ == "__main__":
    main()
