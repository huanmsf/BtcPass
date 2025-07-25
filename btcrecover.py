#!/usr/bin/env python

# btcrecover.py -- Bitcoin wallet password recovery tool
# Copyright (C) 2014-2017 Christopher Gurnee
#
# This program is free software: you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version
# 2 of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see http://www.gnu.org/licenses/

# If you find this program helpful, please consider a small
# donation to the developer at the following Bitcoin address:
#
#           3Au8ZodNHPei7MQiSVAWb7NB2yqsb48GW4
#
#                      Thank You!

# PYTHON_ARGCOMPLETE_OK - enables optional bash tab completion

from __future__ import print_function

from btcrecover import btcrpass
import sys, multiprocessing

if __name__ == "__main__":

    print("Starting", btcrpass.full_version(),
          file=sys.stderr if any(a.startswith("--listp") for a in sys.argv[1:]) else sys.stdout)  # --listpass
    btcrpass.parse_arguments(sys.argv[1:])
    (password_found, not_found_msg) = btcrpass.main()
    
    # 调试信息：显示返回值
    print("DEBUG: password_found =", repr(password_found))
    print("DEBUG: not_found_msg =", repr(not_found_msg))

    if isinstance(password_found, (str, bytes)):
        # 如果是字节字符串，转换为普通字符串
        if isinstance(password_found, bytes):
            password_found = password_found.decode('utf-8', 'replace')
        print("\n==============================\n成功找到密码：'{}'\n==============================\n".format(password_found))
        if any(ord(c) < 32 or ord(c) > 126 for c in password_found):
            print("HTML encoded:   '" + password_found.encode("ascii", "xmlcharrefreplace").decode("ascii") + "'")
        # 写入文件
        with open("result_found.txt", "a", encoding="utf-8") as f:
            wallet_file = None
            for i, arg in enumerate(sys.argv):
                if arg == "--wallet" and i + 1 < len(sys.argv):
                    wallet_file = sys.argv[i + 1]
                    break
            f.write("钱包文件: {}\n密码: {}\n\n".format(wallet_file if wallet_file else "(未知)", password_found))
        retval = 0

    elif not_found_msg:
        print(not_found_msg, file=sys.stderr if btcrpass.args.listpass else sys.stdout)
        retval = 0

    else:
        retval = 1  # An error occurred or Ctrl-C was pressed

    # Wait for any remaining child processes to exit cleanly (to avoid error messages from gc)
    for process in multiprocessing.active_children():
        process.join(1.0)

    sys.exit(retval)
