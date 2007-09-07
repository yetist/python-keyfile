#! /usr/bin/env python
#-*- encoding:utf-8 -*-
#文件名:IniParser.py
"""Test code

Description:________
"""
__version__ = "0.1"
__date__ = "2006年11月18日 星期六 13时57分55秒"
__author__ = "yetist <yetist@gmail.com> "
__license__ = "Licensed under the GPLv2, see the file LICENSE in this tarball."
__copyright__= "Copyright (C) 2006 by yetist <yetist@gmail.com>."

import string
(
        KFILE_NONE,
        KFILE_KEEP_COMMENTS,
        KFILE_KEEP_TRANSLATIONS
        ) = range(3)

class KeyFile:
    def __init__(self):
        self.file_struct = {}
        self.list_separator = ";"
        self.comment_char = "#"
        self.data=""
        self.flag=KFILE_NONE

    def _parse(self):
        found_comm = False
        for line in self.data:
            line = line.strip()
            if not line:
                continue
            #发现注释
            if line[0] == self.comment_char:
                #保留注释
                if self.flag & KFILE_KEEP_COMMENTS:
                    #找到第二行
                    if found_comm:
                        str_comm2 = line[line.index(self.comment_char)+1:].strip()
                        str_comm += str_comm2
                    else:
                        found_comm = True
                        str_comm = line[line.index(self.comment_char)+1:].strip()
                else:
                    continue
            #发现组名
            elif line[0] == "[" and line[-1] == "]":
                group_dict = {}
                group = line[line.find('[')+1:line.find(']')]
                self.file_struct[group]=group_dict
                if found_comm:
                    self.file_struct[group]["comment"]=str_comm
                    found_comm = False
                    str_comm = None
            #发现键值对
            elif line.find("=") >= 0:
                key=line[:line.index("=")].strip()
                value=line[line.index("=")+1:].strip()
                key = key.strip()
                value = value.strip()
                #发现多语言
                if key.find("[") >=0:
                    #保留多语言
                    if self.flag & KFILE_KEEP_TRANSLATIONS:
                        [key,local] = key.split("[")
                        if type(group_dict[key]) == type(""):
                            key_dict={}
                            key_dict["default"] = group_dict[key]
                        else:
                            key_dict = group_dict[key]
                        key_dict[local[:-1]] = value
                        group_dict[key] = key_dict
                    else:
                        continue
                #发现一般键值对
                else:
                    group_dict[key] = value

                if found_comm:
                    if type(group_dict[key]) == type(""):
                        key_dict={}
                        key_dict["default"] = group_dict[key]
                    key_dict["comment"] = str_comm
                    group_dict[key]=key_dict
                    found_comm = False
                    str_comm = None

    def set_list_separator(self, separator):
        self.list_separator = separator

    def load_from_file(self, ini_file, flag=KFILE_NONE):
        self.flag |= flag
        self.data = open(ini_file).readlines()
        self._parse()

    def load_from_data(self, data, flag=KFILE_NONE):
        self.flag |= flag
        self.data = data.splitlines()
        self._parse()

    def to_data(self):
        data = []
        for group in self.get_groups():
            head=[]
            line=[]
            mline=[]
            head.append("[" + group + "]")
            for key in self.get_keys(group):
                val = self.get_value(group, key)
                if key == "comment":
                    if val !="":
                        head.insert(0,self.comment_char+val)
                    continue
                if type(val) == type(""):
                    line.append(key +"="+ val)
                else:
                    tmp=[]
                    for locale in val.keys():
                        val = self.get_locale_string(group,key,locale)
                        if locale == "default":
                            tmp.append(key +"="+ val)
                        elif locale == "comment":
                            tmp.append(self.comment_char+ val)
                        else:
                            tmp.append(key+"["+ locale+ "]="+ val)
                    tmp.sort()
                    mline.extend(tmp)
            data.extend(head)
            data.extend(mline)
            data.extend(line)
        return "\n".join(data)

    def get_start_group(self):
        return self.get_groups()[0]

    def get_groups(self):
        return self.file_struct.keys()

    def get_keys(self, group_name):
        return self.file_struct[group_name].keys()

    def has_group(self, group_name):
        return self.file_struct.has_key(group_name)

    def has_key(self, group_name, key):
        return self.file_struct[group_name].has_key(key)

    def has_locale(self, group_name, key, locale):
        if type(self.file_struct[group_name][key]) == type({}):
            return self.file_struct[group_name][key].has_key(locale)
        else:
            return False

    def get_value(self, group_name, key):
        return self.file_struct[group_name][key]

    def get_string(self, group_name, key):
        if type(self.file_struct[group_name][key]) == type({}):
            return self.file_struct[group_name][key]["default"]
        else:
            return self.file_struct[group_name][key]

    def get_locale_string(self, group_name, key, locale):
        if self.file_struct[group_name][key].has_key(locale):
            return self.file_struct[group_name][key][locale]
        else:
            return ""

    def get_boolean(self, group_name, key):
        ret = self.get_string(group_name, key)
        if ret.lower() in ("t", "true"):
            return True
        else:
            return False

    def get_integer(self, group_name, key):
        ret = self.get_string(group_name, key)
        return int(ret)

    def get_float(self, group_name, key):
        ret = self.get_string(group_name, key)
        return float(ret)

    def get_string_list(self, group_name, key):
        ret = self.get_string(group_name, key)
        return ret.split(self.list_separator)

    def get_locale_string_list(self, group_name, key, locale):
        ret = self.get_locale_string(group_name, key, locale)
        return ret.split(self.list_separator)

    def get_boolean_list(self, group_name, key):
        ret = self.get_string_list(group_name, key)
        lst=[]
        for i in ret:
            if i.lower() in ("t", "true", "1"):
                lst.append(True)
            else:
                lst.append(False)
        return lst

    def get_integer_list(self, group_name, key):
        ret = self.get_string_list(group_name, key)
        return [int(i) for i in ret]

    def get_float_list (self, group_name, key):
        ret = self.get_string_list( group_name, key)
        return [float(i) for i in ret]

    def get_comment(self, group_name, key):
        return self.file_struct[group_name][key]["comment"]

    def set_value(self, group_name, key, value):
        if not self.has_group(group_name):
            self.file_struct[group_name] = {}
        self.file_struct[group_name][key] = value

    def set_string(self, group_name, key, string):
        if not self.has_group(group_name):
            self.file_struct[group_name] = {}
        if not self.has_key(group_name,key):
            self.file_struct[group_name][key] = str(string)

        elif type(self.file_struct[group_name][key]) == type({}):
            self.file_struct[group_name][key]["default"] = str(string)

    def set_locale_string(self, group_name, key, locale, string):
        if not self.has_group(group_name):
            self.file_struct[group_name] = {}

        if type(self.file_struct[group_name][key]) == type({}):
            self.file_struct[group_name][key][locale] = str(string)
        else:
            key_dict = {}
            key_dict["default"] = self.file_struct[group_name][key]
            key_dict[locale] = str(string)
            self.file_struct[group_name][key] = key_dict


    def set_boolean(self, group_name, key, value):
        if not self.has_group(group_name):
            self.file_struct[group_name] = {}
        if value:
            self.file_struct[group_name][key] = "True"
        else:
            self.file_struct[group_name][key] = "False"

    def set_integer(self, group_name, key, value):
        if not self.has_group(group_name):
            self.file_struct[group_name] = {}
        self.file_struct[group_name][key] = str(value)

    def set_float(self, group_name, key, value):
        if not self.has_group(group_name):
            self.file_struct[group_name] = {}
        self.file_struct[group_name][key] = str(value)

    def set_string_list(self, group_name, key, list):
        if not self.has_group(group_name):
            self.file_struct[group_name] = {}
        value = self.list_separator.join(list)
        self.file_struct[group_name][key] = value

    def set_locale_string_list(self, group_name, key, locale, list):
        if not self.has_group(group_name):
            self.file_struct[group_name] = {}
        if not self.has_key(group_name, key):
            self.file_struct[group_name][key] = {}
        value = self.list_separator.join(list)
        self.file_struct[group_name][key][locale] = value

    def set_boolean_list(self, group_name, key, list):
        if not self.has_group(group_name):
            self.file_struct[group_name] = {}
        value = self.list_separator.join([str(i) for i in list])
        self.file_struct[group_name][key] = value

    def set_integer_list(self, group_name, key, list):
        if not self.has_group(group_name):
            self.file_struct[group_name] = {}
        value = self.list_separator.join([str(i) for i in list])
        self.file_struct[group_name][key] = value

    def set_float_list(self, group_name, key, list):
        if not self.has_group(group_name):
            self.file_struct[group_name] = {}
        value = self.list_separator.join([str(i) for i in list])
        self.file_struct[group_name][key] = value

    def set_comment(self, group_name, key, comment):
        if not self.has_group(group_name):
            self.file_struct[group_name] = {}
        if key is None:
            self.file_struct[group_name]["comment"] = comment
            return
        if not self.has_key(group_name, key):
            key_dict={}
        elif type(self.file_struct[group_name][key]) == type(""):
            key_dict={}
            key_dict["default"] = self.file_struct[group_name][key]

        elif type(self.file_struct[group_name][key]) == type({}):
            key_dict = self.file_struct[group_name][key]

        key_dict["comment"] = comment
        self.file_struct[group_name][key] = key_dict

    def remove_group(self, group_name):
        self.file_struct.pop(group_name)

    def remove_key(self, group_name, key):
        self.file_struct[group_name].pop(key)

    def remove_comment(self, group_name, key):
        self.file_struct[group_name][key].pop("comment")

if __name__=="__main__":
    #a=KeyFile()
    #a.comment_char="#"
    ##flag = KFILE_NONE
    ##flag = KFILE_KEEP_COMMENTS
    #flag = KFILE_KEEP_TRANSLATIONS
    ##flag = KFILE_KEEP_COMMENTS|KFILE_KEEP_TRANSLATIONS
    #a.load_from_file("/usr/share/applications/gedit.desktop",flag)
    #a.load_from_file("/etc/php/apache2-php5/php.ini",flag)


    #print "################################################################################"
    #print a.to_data()
    import sys
    print >>sys.stderr, "Error! The file can't be run!\n"

