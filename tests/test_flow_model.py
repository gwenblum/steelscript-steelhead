# Copyright (c) 2015 Riverbed Technology, Inc.
#
# This software is licensed under the terms and conditions of the MIT License
# accompanying the software ("License").  This software is distributed "AS IS"
# as set forth in the License.

from __future__ import (absolute_import, unicode_literals, print_function,
                        division)

from unittest import mock
import pytest
from ipaddress import IPv4Address, IPv6Address

from steelscript.steelhead.features.flows.v8_5.model import FlowsModel\
    as CommonFlows


SHOW_FLOWS_ALL_OUTPUT = """\
T  Source                Destination           App     Rdn Since
--------------------------------------------------------------------------------
N  10.190.0.1:406        10.190.5.2:1003       UDPv4   99% 2014/02/10 23:58:01
O  192.168.0.1:80        192.168.5.1:80        SRDF_V2 11% 2014/02/01 00:00:01
O  192.168.221.1:1080    192.168.221.1:1080    CIFS     0% 2014/02/01 00:20:01
O  192.168.221.1:443     192.168.221.1:443     MAPI    99% 2014/02/01 00:21:01
N  192.168.221.1:1443    192.168.221.1:5543    TCPv4   99% 2014/02/10 23:56:01
N  10.190.0.1:1406       10.190.5.2:2003       FTP-DAT 59% 2014/02/01 00:00:01
N  [10::190:f0:1]:146    [10::190:e5:2]:203    FTP-DAT 20% 2014/02/01 10:10:11
N  11.19.11.11:146       10.190.11.11:3003     UDPv4    0% pre_existing
--------------------------------------------------------------------------------
                                           All    V4     V6
---------------------------------------------------------------
Established Optimized:                     1      2      3

  RiOS Only (O):                           1      3      3
  SCPS Only (SO):                          11     22     33
  RiOS+SCPS (RS):                          1      2      3
  TCP Proxy (TP):                          1      2      3
  Packet-mode optimized (N):               11     22     33

Half-opened optimized (H):                 1      2      3
Half-closed optimized (C):                 11     22     33

Establishing (E):                          1      2      3
Passthrough :                              11     22     33

  Passthrough intentional (PI):            1      2      3
  Passthrough unintentional (PU):          11     22     33

    Terminated:                            1      2      3
    Packet-mode:                           11     22     33

Forwarded (F):                             1      2      3
Discarded (terminated):                    1
Denied (terminated):                       1
---------------------------------------------------------------

Total:                                     11     40      70
"""


SHOW_FLOWS_ALL_PARSED_DICT = {
    'flows_list': [
        {'app': 'UDPv4',
         'destination ip': IPv4Address('10.190.5.2'),
         'destination port': 1003,
         'reduction': 99,
         'since': {'day': '10',
                   'hour': '23',
                   'min': '58',
                   'month': '02',
                   'secs': '01',
                   'year': '2014'},
         'source ip': IPv4Address('10.190.0.1'),
         'source port': 406,
         'type': 'N'},
        {'app': 'SRDF_V2',
         'destination ip': IPv4Address('192.168.5.1'),
         'destination port': 80,
         'reduction': 11,
         'since': {'day': '01',
                   'hour': '00',
                   'min': '00',
                   'month': '02',
                   'secs': '01',
                   'year': '2014'},
         'source ip': IPv4Address('192.168.0.1'),
         'source port': 80,
         'type': 'O'},
        {'app': 'CIFS',
         'destination ip': IPv4Address('192.168.221.1'),
         'destination port': 1080,
         'reduction': 0,
         'since': {'day': '01',
                   'hour': '00',
                   'min': '20',
                   'month': '02',
                   'secs': '01',
                   'year': '2014'},
         'source ip': IPv4Address('192.168.221.1'),
         'source port': 1080,
         'type': 'O'},
        {'app': 'MAPI',
         'destination ip': IPv4Address('192.168.221.1'),
         'destination port': 443,
         'reduction': 99,
         'since': {'day': '01',
                   'hour': '00',
                   'min': '21',
                   'month': '02',
                   'secs': '01',
                   'year': '2014'},
         'source ip': IPv4Address('192.168.221.1'),
         'source port': 443,
         'type': 'O'},
        {'app': 'TCPv4',
         'destination ip': IPv4Address('192.168.221.1'),
         'destination port': 5543,
         'reduction': 99,
         'since': {'day': '10',
                   'hour': '23',
                   'min': '56',
                   'month': '02',
                   'secs': '01',
                   'year': '2014'},
         'source ip': IPv4Address('192.168.221.1'),
         'source port': 1443,
         'type': 'N'},
        {'app': 'FTP-DAT',
         'destination ip': IPv4Address('10.190.5.2'),
         'destination port': 2003,
         'reduction': 59,
         'since': {'day': '01',
                   'hour': '00',
                   'min': '00',
                   'month': '02',
                   'secs': '01',
                   'year': '2014'},
         'source ip': IPv4Address('10.190.0.1'),
         'source port': 1406,
         'type': 'N'},
        {'app': 'FTP-DAT',
         'destination ip': IPv6Address('10::190:e5:2'),
         'destination port': 203,
         'reduction': 20,
         'since': {'day': '01',
                   'hour': '10',
                   'min': '10',
                   'month': '02',
                   'secs': '11',
                   'year': '2014'},
         'source ip': IPv6Address('10::190:f0:1'),
         'source port': 146,
         'type': 'N'},
        {'app': 'UDPv4',
         'destination ip': IPv4Address('10.190.11.11'),
         'destination port': 3003,
         'reduction': 0,
         'since': {'pre_existing': True},
         'source ip': IPv4Address('11.19.11.11'),
         'source port': 146,
         'type': 'N'}
    ],
    'flows_summary': {
        'denied': {'all': 1},
        'discarded': {'all': 1},
        'establishing': {'all': 1, 'v4': 2, 'v6': 3},
        'forwarded': {'all': 1, 'v4': 2, 'v6': 3},
        'half_closed optimized': {'all': 11, 'v4': 22, 'v6': 33},
        'half_opened optimized': {'all': 1, 'v4': 2, 'v6': 3},
        'established optimized': {'all': 1, 'v4': 2, 'v6': 3},
        'packet_mode optimized': {'all': 11, 'v4': 22, 'v6': 33},
        'passthrough': {'all': 11, 'v4': 22, 'v6': 33},
        'passthrough intentional': {'all': 1, 'v4': 2, 'v6': 3},
        'passthrough unintentional': {'all': 11, 'v4': 22, 'v6': 33},
        'passthrough unintentional packet_mode': {'all': 11,
                                                  'v4': 22,
                                                  'v6': 33},
        'passthrough unintentional terminated': {'all': 1, 'v4': 2, 'v6': 3},
        'rios only': {'all': 1, 'v4': 3, 'v6': 3},
        'rios scps': {'all': 1, 'v4': 2, 'v6': 3},
        'scps only': {'all': 11, 'v4': 22, 'v6': 33},
        'tcp proxy': {'all': 1, 'v4': 2, 'v6': 3},
        'total': {'all': 11, 'v4': 40, 'v6': 70}}
}


@pytest.yield_fixture
def mock_cli(request):
    with mock.patch('steelscript.common.interaction.model.Model.cli') as cli:
        yield cli


def test_show_flows(mock_cli):
    model = CommonFlows(mock.Mock(), cli=mock_cli)
    mock_cli.exec_command.return_value = SHOW_FLOWS_ALL_OUTPUT
    result = model.show_flows()
    assert result['flows_list'] == SHOW_FLOWS_ALL_PARSED_DICT['flows_list']
    assert result['flows_summary'] == \
        SHOW_FLOWS_ALL_PARSED_DICT['flows_summary']
