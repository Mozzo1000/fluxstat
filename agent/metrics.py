import psutil
import os

class CPU():
    def __init__(self):
        core_count = os.cpu_count()
        cpu_usage_total = psutil.cpu_percent(1) # TODO: Look into how to remove the need to block
        cpu_usage_total_percpu = psutil.cpu_percent(percpu=True)
        cpu_cores = {}

        for index, core in enumerate(cpu_usage_total_percpu):
            cpu_cores["cpu_" + str(index)] = core

        self.data = {
            "cpu_core_total": core_count,
            "cpu_usage_percentage": cpu_usage_total,
            "cpu_core_usage_percentage": cpu_cores
        }
    
    def toJSON(self):
        return self.data

class Memory():
    def __init__(self):
        memory_free = psutil.virtual_memory().free
        memory_used = psutil.virtual_memory().used
        memory_total = psutil.virtual_memory().total
        memory_used_percentage = round(psutil.virtual_memory().percent)

        self.data = {
            "memory_free": memory_free,
            "memory_used": memory_used,
            "memory_total": memory_total,
            "memory_used_percentage": memory_used_percentage
        }

    def toJSON(self):
        return self.data

class Disk():
    def __init__(self):
        all_disks = psutil.disk_partitions()
        disks = {}
        for index, disk in enumerate(all_disks):
            usage_info = psutil.disk_usage(disk.mountpoint)
            disks["disk_" + str(index)] = {
                "name": disk.device,
                "mount": disk.mountpoint,
                "filesystem": disk.fstype,
                "usage": {
                    "total": usage_info.total,
                    "free": usage_info.free,
                    "used": usage_info.used,
                    "used_percentage": round(usage_info.percent)
                }
            }

        self.data = {
            "disks_total": len(all_disks),
            "disks": disks
        }

    def toJSON(self):
        return self.data