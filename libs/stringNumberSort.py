# -*- coding: utf-8 -*-
import re

def sort_key(s):
    # 排序关键字匹配
    # 匹配开头数字序号
    if s:
        try:
            c = re.findall('^\d+', s.name)[0]
        except:
            c = -1
        return int(c)

def strsort(alist):
    alist.sort(key=sort_key)
    return alist


if __name__ == "__main__":
    a = ['0preface', '0toc', '10cpu-sched-multi', '11cpu-dialogue', '12dialogue-vm', '13vm-intro', '14vm-api', '15vm-mechanism', '16vm-segmentation', '17vm-freespace', '18vm-paging', '19vm-tlbs', '1dialogue-threeeasy', '20vm-smalltables', '21vm-beyondphys', '22vm-beyondphys-policy', '23vm-vax', '24vm-dialogue', '2intro', '3dialogue-virtualization', '4cpu-intro', '5cpu-api', '6cpu-mechanisms', '7cpu-sched', '8cpu-sched-mlfq', '9cpu-sched-lottery', '25dialogue-concurrency', '26threads-intro', '27threads-api', '28threads-locks', '29threads-locks-usage',
         '30threads-cv', '31threads-sema', '32threads-bugs', '33threads-events', '34threads-dialogue', '35dialogue-persistence', '36file-devices', '37file-disks', '38file-raid', '39file-intro', '40file-implementation', '41file-ffs', '42file-journaling', '43file-lfs', '44file-integrity', '45file-dialogue', '46dialogue-distribution', '47dist-intro', '48dist-nfs', '49dist-afs', '50dist-dialogue', 'dialogue-labs', 'dialogue-monitors', 'dialogue-vmm', 'file-ssd', 'lab-projects-systems', 'lab-projects-xv6', 'lab-tutorial', 'threads-monitors', 'vmm-intro']

    print(strsort(a))