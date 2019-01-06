# -*- coding: utf-8 -*-


def cgr(first, last, periods):
    return (last / first) ** (1 / float(periods)) * 100.0 - 100.0
