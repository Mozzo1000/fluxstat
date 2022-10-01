# ![alt text](assets/icon.png  "fluxstat logo") fluxstat
A system metrics exporter intended for devices on a local and small network. `fluxstat` uses a JSON based system for exposing metric data and intentionally does **NOT** use the [OpenMetrics](https://openmetrics.io/) standard.

## Exposed metrics
`fluxstat` exposes a `/metrics` endpoint over HTTP.
A `updated_at` property in the response shows when the data was retrieved.

### Uptime
`uptime` property is shown in seconds.

### CPU
* `cpu_core_total`
  * Number of processor cores (both logical and physical).
* `cpu_usage_percentage`
  * The percentage of current processor usage.
* `cpu_core_usage_percentage`
  * Shows percentage of current processor usage per core. Each core is named `cpu_X` in which `X` is a number starting from 0.

### Memory
* `memory_free`
  * Amount of free memory shown in bytes.
* `memory_used`
  * Amount of used memory shown in bytes.
* `memory_total`
  * Total amount of memory in the system shown in bytes.
* `memory_used_percentage`
  * Percentage of used memory.

### Disk
* `disks_total`
  * Number of storage devices detected.
* `disks`
  * A list of storage devices named `disk_X` in which `X` is a number starting from 0.
  * Inside of each `disk_X` there is `name`, `mount` and `filesystem` properties alongside usage data.

### Example
```json
{
  "system": {
    "uptime: ": 947578,
    "cpu": {
      "cpu_core_total": 4,
      "cpu_usage_percentage": 25.8,
      "cpu_core_usage_percentage": {
        "cpu_0": 28.7,
        "cpu_1": 29.2,
        "cpu_2": 24.6,
        "cpu_3": 28.6
      }
    },
    "memory": {
      "memory_free": 9904599040,
      "memory_used": 7214452736,
      "memory_total": 17119047680,
      "memory_used_percentage": 42
    },
    "disk": {
      "disks_total": 1,
      "disks": {
        "disk_0": {
          "name": "C:\\",
          "mount": "C:\\",
          "filesystem": "NTFS",
          "usage": {
            "total": 255482392576,
            "free": 62549286912,
            "used": 192933105664,
            "used_percentage": 76
          }
        }
      }
    }
  },
  "updated_at": "2022-10-01T18:14:39.682011"
}
```
*This example was collected on Windows 10 and shows a processor with four (4) cores and with one (1) storage device installed.*

## Compatibility
The aim is to support `Windows`, `Mac` and `Linux` but at the moment not all operating systems have been tested. 
`fluxstat` has been developed with `Python 3.10`.


### Tested operating systems 
| Operating system | Version | 
| -----------------|:--------|
| Windows 10       | 21H1    |


## License
`fluxstat` is licensed under the Apache License, Version 2.0. See [LICENSE](LICENSE) for the full license text.