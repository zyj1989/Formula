#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Create Date: 2016-07-29 15:19
# Author: Airlam


class IllegalStringException(Exception):

    def __init__(self, message, origin_s, pos, max_show_length=100, mode=1):
        super(IllegalStringException, self).__init__(self)
        self.message = message
        pos = min(pos, len(origin_s))
        show_origin_s = False
        origin_s_length = len(origin_s)
        if origin_s_length > max_show_length:
            show_origin_s = True

        max_prefix_show_length = max_show_length / 2
        max_suffix_show_length = max_show_length - max_prefix_show_length

        if pos < max_prefix_show_length:
            max_suffix_show_length = max_show_length - pos
        if origin_s_length - pos < max_suffix_show_length:
            max_prefix_show_length = max_show_length - (origin_s_length - pos)

        if pos > max_prefix_show_length:
            prefix_s = u'...{}'.format(origin_s[pos - max_prefix_show_length + 3:pos])
            arrow_pos = max_prefix_show_length
        else:
            prefix_s = origin_s[:pos]
            arrow_pos = pos

        if pos < len(origin_s) - max_suffix_show_length:
            suffix_s = u'{}...'.format(origin_s[pos:pos + max_suffix_show_length - 3])
        else:
            suffix_s = origin_s[pos:]

        if mode == 0:
            sample_s = prefix_s + suffix_s + u'\n'
            self.present_s = u'{}\n{}{}{}'.format(self.message,
                                                  origin_s + u'\n' if show_origin_s else u'',
                                                  sample_s,
                                                  u' ' * arrow_pos + u'^').encode('utf-8')
        elif mode == 1:
            sample_s = prefix_s + u'\n' + u' ' * arrow_pos + suffix_s
            self.present_s = u'{}\n{}{}'.format(self.message,
                                                origin_s + u'\n' if show_origin_s else u'',
                                                sample_s).encode('utf-8')

    def __str__(self):
        return self.present_s

