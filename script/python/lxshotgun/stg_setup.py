# coding:utf-8
import os

def start_toolkit_classic():
    import sgtk

    logger = sgtk.LogManager.get_logger(__name__)

    logger.debug("Launching toolkit in classic mode.")

    # Get the name of the engine to start from the environement
    env_engine = os.environ.get("SGTK_ENGINE")
    if not env_engine:
        return

    # Get the context load from the environment.
    env_context = os.environ.get("SGTK_CONTEXT")
    if not env_context:
        return
    try:
        # Deserialize the environment context
        context = sgtk.context.deserialize(env_context)
    except Exception as e:
        return

    try:
        # Start up the toolkit engine from the environment data
        logger.debug(
            "Launching engine instance '%s' for context %s" % (env_engine, env_context)
        )
        sgtk.platform.start_engine(env_engine, context.sgtk, context)
    except Exception as e:
        return


def start_toolkit():
    import sgtk

    # start up toolkit logging to file
    sgtk.LogManager().initialize_base_file_handler("tk-maya")

    start_toolkit_classic()

    # Clean up temp env variables.
    del_vars = [
        "SGTK_ENGINE",
        "SGTK_CONTEXT",
        "SGTK_FILE_TO_OPEN",
        "SGTK_LOAD_MAYA_PLUGINS",
    ]
    for var in del_vars:
        if var in os.environ:
            del os.environ[var]


class ShotgunSetup(object):
    def set_run(self):
        pass