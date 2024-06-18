# prtg_prometheus_exporter

Export PRTG Online/Offline status for use with Prometheus/Grafana

**How to use:******

**Open prtg-exporter.py** and add your API key and endpoint



**Add this into your prometheus config:**
```
  - job_name: "prtg"
    static_configs:
      - targets: ["localhost:3310"]
    scrape_interval: 120s
    scrape_timeout: 40s
    metrics_path: /metrics
```

**Run prtg-exporter.py**

**Launch Prometheus**

**Prometheus will now load data**


# Examples of final product:

**Exporter running**

![image](https://github.com/saadmh902/yodeck-prometheus-exporter/assets/49423626/d4b379fb-0cb7-450f-9377-8f6ee8694a6c)


**Grafana Example**

![image](https://github.com/saadmh902/yodeck-prometheus-exporter/assets/49423626/9bd98f11-7462-49df-9329-0e1361f42b6c)

**Prometheus Scraping**

![image](https://github.com/saadmh902/yodeck-prometheus-exporter/assets/49423626/1a9d1f37-c16b-4284-b81c-d3cd0d4227a1)
