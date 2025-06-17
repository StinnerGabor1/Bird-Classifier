import h5py
import json

with h5py.File("model 2.h5", "r+") as f:
    config_str = f.attrs["model_config"]
    config_dict = json.loads(config_str)

    def update_rotation_factor(cfg):
        if isinstance(cfg, dict):
            if cfg.get("class_name") == "RandomRotation":
                print("OK")
                cfg["config"]["factor"] = 0.4  # Change this value as needed
            for key in cfg:
                update_rotation_factor(cfg[key])
        elif isinstance(cfg, list):
            for item in cfg:
                update_rotation_factor(item)

    update_rotation_factor(config_dict)

    # Overwrite with updated config
    f.attrs["model_config"] = json.dumps(config_dict).encode("utf-8")