import sigar


def prefix(prefix):
    def outer(method):
        def wrapper(*args, **kargs):
            info = method(*args, **kargs)
            return dict((prefix + k, v)for k, v in info.iteritems())
        return wrapper
    return outer


class Collector(object):

    def __init__(self):
        self.sigar = sigar.open()

    def __del__(self):
        self.sigar.close()

    @prefix("mem_")
    def get_mem_stats(self):
        mem = self.sigar.mem()
        return {
            "ram": mem.ram() * 1024**2,
            "total": mem.total(),
            "used": mem.used(),
            "free": mem.free(),
            "actual_free": mem.actual_free(),
            "actual_used": mem.actual_used(),
            "free_percent": mem.free_percent(),
            "used_percent": mem.used_percent(),
        }

    @prefix("cpu_")
    def get_cpu_stats(self):
        cpu = self.sigar.cpu()
        total = float(cpu.total())
        return {
            "idle": cpu.idle() / total,
            "nice": cpu.nice() / total,
            "stolen": cpu.stolen() / total,
            "sys": cpu.sys() / total,
            "user": cpu.user() / total,
            "wait": cpu.wait() / total,
        }

    @prefix("swap_")
    def get_swap_stats(self):
        swap = self.sigar.swap()
        return {
            "free": swap.free(),
            "used": swap.used(),
            "total": swap.total(),
            "page_in": swap.page_in(),
            "page_out": swap.page_out(),
        }

    def get_all_stats(self):
        stats = {}
        stats.update(self.get_mem_stats())
        stats.update(self.get_cpu_stats())
        stats.update(self.get_swap_stats())
        return stats
