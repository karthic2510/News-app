import json
from flask import Flask, request, jsonify

input = f"Summary: Mixed Results for US Market as Investors React to Monetary Policy and Earnings Reports.\n US futures are up after a larger-than-expected increase in jobless claims. The market finished mixed yesterday after a sharp decline caused by the Federal Reserve. Seeking Alpha contributors advise investors to be positioned conservatively given the impact tighter monetary policy will have on the economy until 2024. Disappointing third-quarter results lead Carvana shares to fall by 42.9%, while MongoDB soared 23.2% after posting better-than-expected Q3 revenue and issuing positive Q4 revenue guidance. State Street's shares also jumped 8.2% following a new buyback plan announcement, and homebuilder Toll Brothers saw its shares rise by 7.8% after posting better-than-expected quarterly results. MongoDB's shares surged 26% in after-hours trading following an upbeat quarterly report, and the company plans to hire more employees as it pushes into Indian markets and expands its features such as queryable encryption and relational migrator."

print(json.dumps(input))