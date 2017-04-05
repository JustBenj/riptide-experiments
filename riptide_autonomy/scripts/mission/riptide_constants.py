class RiptideConstants:
    ACCEL_COMMAND_TOPIC = "command/accel"

    # Accelerations for each axis in meters per second
    # TODO: This is an assumed value. Actual values need to be determined experimentally
    LINEAR_X_ACCEL = 1.0
    LINEAR_Y_ACCEL = 1.0
    LINEAR_Z_ACCEL = 1.0

    ANGULAR_X_ACCEL = 1.0
    ANGULAR_Y_ACCEL = 1.0
    ANGULAR_Z_ACCEL = 1.0

    COMMAND_TRANSLATE_X_POS = "tx+"
    COMMAND_TRANSLATE_Y_POS = "ty+"
    COMMAND_TRANSLATE_Z_POS = "tz+"
    COMMAND_ROTATE_X_CW = "rx+"
    COMMAND_ROTATE_Y_CW = "ry+"
    COMMAND_ROTATE_Z_CW = "rz+"

    COMMAND_TRANSLATE_X_NEG = "tx-"
    COMMAND_TRANSLATE_Y_NEG = "ty-"
    COMMAND_TRANSLATE_Z_NEG = "tz-"
    COMMAND_ROTATE_X_CCW  = "rx-"
    COMMAND_ROTATE_Y_CCW = "ry-"
    COMMAND_ROTATE_Z_CCW = "rz-"
