# coding:utf-8
import lxutil.dcc.dcc_objects as utl_dcc_objects


class FileCollection(object):
    def __init__(self, source_path, target_path):
        d = utl_dcc_objects.OsDirectory_(source_path)
        dds = d.get_descendants()
        dic = {}
        for dd in dds:
            fps = dd.get_child_file_paths()
            for fp in fps:
                # print fp
                sfp = fp[len(source_path):]
                # print sfp
                sf = utl_dcc_objects.OsFile(sfp)
                if sfp.endswith('.tx'):
                    osfp = sf.get_orig_file('.tx')
                    if osfp is not None:
                        osf = utl_dcc_objects.OsFile(osfp)
                        fn = osf.name
                        if fn in dic:
                            seq = dic[fn]
                            seq += 1
                            dic[fn] = seq
                            new_fn = '{}.v{}{}'.format(osf.base, str(seq).zfill(3), osf.ext)
                        else:
                            seq = 0
                            dic[fn] = seq
                            new_fn = fn
                        target_file_path = '{}/image/{}'.format(target_path, new_fn)
                        osf.set_copy_to_file(target_file_path)
                elif sfp.endswith('.abc'):
                    target_file_path = '{}/abc/{}'.format(target_path, sf.name)
                    sf.set_copy_to_file(target_file_path)


if __name__ == '__main__':
    print utl_dcc_objects.OsFile(
        '/l/temp/td/dongchangbao/tx_convert_test/exr_1/jiguang_cloth_mask.1001.1001.tx'
    ).get_orig_file('.tx')
    # FileCollection(
    #     source_path='/data/package_temporary_bsnw_1',
    #     target_path='/data/package_temporary_bsnw_1_0',
    # )
