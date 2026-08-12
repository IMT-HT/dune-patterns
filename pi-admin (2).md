# Pi Admin's Minimal Guide — duneweaver.local

For the keeper of one Raspberry Pi Zero 2 W running Dune Weaver. Everything here is
typed into Terminal after: `ssh <user>@duneweaver.local` (password from the index
card). Exit any SSH session with `exit` or closing the window — both are safe.

---

## The five commands that are 95% of the job

| You want to… | Type |
|---|---|
| Turn it off properly | `sudo shutdown now` → wait for LED to stop → unplug |
| Restart it | `sudo reboot` (drops your SSH; reconnect in ~1 min) |
| Check disk space | `df -h` (look at the `/` line; worry only past ~85%) |
| Check temperature | `vcgencmd measure_temp` (idle 40–55°C fine; 70s = investigate airflow) |
| How long has it been up | `uptime` |

`sudo` = "do it with authority"; it may re-ask your password. That's normal.

## The Dune Weaver service (runs in Docker)

The app lives in a Docker container the setup script created. *(Verify the folder
name on first look: `ls ~` — expect `dune-weaver`; adjust paths below if different.)*

| Situation | Type |
|---|---|
| UI not loading but Pi answers SSH | `cd ~/dune-weaver && docker compose restart` |
| See what the app is saying (logs) | `cd ~/dune-weaver && docker compose logs --tail 50` |
| Is the container running? | `docker ps` (expect a dune-weaver entry, status "Up") |
| **Software updates** | **Don't use the terminal — Settings page in the UI has one-click update.** |

## Triage ladder (when something's wrong, in order)

1. **Phone can't reach duneweaver.local** → is the phone on the same WiFi (the 2.4
   network)? → try `http://duneweaver.local` typed fully → still no: find the Pi's
   IP in your router's device list and browse to `http://<that-ip>`.
2. **IP works but .local doesn't** → cosmetic name-resolution sulk; reboot the Pi
   once, or just use the IP.
3. **Nothing answers, SSH refused too** → power cycle (pull plug, wait 10s, plug
   in, wait 2 min). This is legal; see power rules.
4. **Power cycle doesn't revive it** → SD card into the reader, look at it on the
   Mac (does it mount?). Worst case = reflash per the build sheet's Phase A/C —
   30 min, patterns in the stock library return automatically; custom patterns
   re-upload from your files. Annoying, never fatal.

## Power rules (the whole doctrine)

- **Steady state: leave it plugged in forever.** It sips ~2W; the .local address
  and the future bridge both want it always-on.
- **Planned unplug:** `sudo shutdown now` first when convenient.
- **Yank when needed:** fine while idle. The ONE bad moment: mid-update or during
  a long install — never pull power while the Settings page says it's updating.

## Rare but useful

- Change WiFi / hostname / password later: `sudo raspi-config` (menu-driven, arrow
  keys, no memorization).
- OS-level updates (`sudo apt update && sudo apt full-upgrade`): optional, quarterly
  at most; the app updates itself through its own UI and doesn't need this.
- Back up custom patterns before any reflash: they live under the app folder
  (`~/dune-weaver/patterns/custom_patterns/` — *verify path*); copy off with
  `scp` or just re-upload from your Mac's copies, which is easier.

## What NOT to do

- No `sudo` commands from internet strangers without asking Ashlar first.
- Don't edit files inside the app folder by hand — the UI and the future bridge
  script are the two sanctioned writers.
- Don't fix what isn't broken. An always-on Pi that answers its name needs nothing
  from you but electricity and the occasional glance at the temperature.

*Living document — expand as reality teaches. v0, written before the board arrived.*
