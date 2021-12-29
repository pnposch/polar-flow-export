Polar Flow Exporter
===================

A tool for exporting training sessions from [Polar Flow](https://flow.polar.com).

## Installation

```bash
$ git clone https://github.com/pnposch/polar-flow-export.git
$ docker-compose up -d
```


## Usage

```bash
docker exec -it polar-flow-export python3 polar-flow-export.py
```

The tool will save sessions into the output directory, using the default filename
provided by Polar.

## Explanation

Annoyingly, the Polar Accesslink API doesn't provide access to historical training
data, only new sessions. This means that if you've just created, for example, a
Strava account, you have to manually export and upload each session in order to
have all your old data show on your Strava account. Even more annoyingly, all the
existing Polar Flow export tools I found were clearly written prior to an extensive
rewrite of the website, which now uses React under the hood. Therefore, they no
longer work.

I originally wanted to use `https://flow.polar.com/diary/training-list` to fetch
all the IDs, but they're cleverly hidden inside onClick attributes that have
prebound arguments, so I got tired of trying this route (may revisit later - using
React DevTools, it's possible to inspect them and find the ID under `[[BoundArgs]]`,
so perhaps possible to do programatically using Selenium).

Instead, the IDs are available on `https://flow.polar.com/diary`, but the page
is only rendered properly with Javascript, so simply using `requests` wouldn't
work, which is why I wrote this tool using Selenium.

Anyway, rant over.
