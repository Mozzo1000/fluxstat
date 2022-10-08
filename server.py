import argparse
from threading import Timer
import urllib.request
import json
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS

def main():
    parser = argparse.ArgumentParser("Fluxstat Server")
    parser.add_argument("-i", "--interval", type=int, default=5, help="How often to retrieve metrics from agents in seconds")
    parser.add_argument("-a", "--agent", type=str, nargs="+", default=["localhost"], help="IP address of agent(s) to retrieve metrics from. Multiple can be listed at the same time.")

    db_group = parser.add_argument_group("Database arguments")
    db_group.add_argument("--db-url", type=str, default="http://localhost:8086", help="URL of InfluxDB instance")
    db_group.add_argument("--db-token", type=str, required=True, help="API token for InfluxDB instance")
    db_group.add_argument("--db-org", type=str, required=True, help="InfluxDB organization")
    db_group.add_argument("--db-bucket", type=str, required=True, help="Bucket of InfluxDB instance")

    print(parser.parse_args().agent)

    for i in parser.parse_args().agent:
        get_metrics(parser, i)

def get_metrics(parser, url):
        interval = parser.parse_args().interval

        bucket = parser.parse_args().db_bucket
        client = InfluxDBClient(url=parser.parse_args().db_url, token=parser.parse_args().db_token, org=parser.parse_args().db_org)
        write_api = client.write_api(write_options=SYNCHRONOUS)

        thread = Timer(interval, get_metrics, [parser, url])
        thread.start()
        print("Getting metrics : " + url)
        with urllib.request.urlopen(url + "/metrics") as response:
            data = json.loads(response.read().decode("utf-8"))
            
            p = Point(url).field("uptime", data["system"]["uptime"])\
                .field("cpu_usage", data["system"]["cpu"]["cpu_usage_percentage"])\
                .field("memory_free", data["system"]["memory"]["memory_free"])\
                .field("memory_used", data["system"]["memory"]["memory_used"])\
                .field("memory_total", data["system"]["memory"]["memory_total"])\
                .field("memory_used_percentage", data["system"]["memory"]["memory_used_percentage"])

            # Loop over all cpu cores and add data to field
            for core in data["system"]["cpu"]["cpu_core_usage_percentage"]:
                p.field(core, data["system"]["cpu"]["cpu_core_usage_percentage"][core])

            # Loop over all storage devices and add data to fields
            for disk in data["system"]["disk"]["disks"]:
                p.field(disk + "_usage_total", data["system"]["disk"]["disks"][disk]["usage"]["total"])
                p.field(disk + "_usage_free", data["system"]["disk"]["disks"][disk]["usage"]["free"])
                p.field(disk + "_usage_used", data["system"]["disk"]["disks"][disk]["usage"]["used"])
                p.field(disk + "_usage_used_percentage", data["system"]["disk"]["disks"][disk]["usage"]["used_percentage"])

            write_api.write(bucket=bucket, record=p)

if __name__ == "__main__":
    main()

