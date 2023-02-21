# coding:utf-8
import lxutil.etr.abstracts as utl_etr_abstracts


class ScpUsd(utl_etr_abstracts.AbsScpUsd):
    def registry_set(self, file_path):
        # noinspection PyUnresolvedReferences
        import production.gen.record_set_registry as pgs
        pgs.run(file_path)
