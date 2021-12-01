# coding:utf-8
# noinspection PyUnresolvedReferences

def set_script_clear():
    for i in cmds.scriptJob(listJobs=1):
        for k in ['leukocyte.antivirus()']:
            if k in i:
                print 'remove script job {}'.format(k)
                index = i.split(': ')[0]
                cmds.scriptJob(kill=int(index), force=1)

    for i in cmds.ls(type='script'):
        if i in ['breed_gene', 'vaccine_gene']:
            print 'remove script node {}'.format(i)
            cmds.delete(i)
