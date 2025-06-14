import h5py
import json

with h5py.File("model.h5", "r+") as f:
    config_str = f.attrs["model_config"]
    config_dict = json.loads(config_str)

    def remove_data_format(cfg):
        if isinstance(cfg, dict):
            if cfg.get("class_name") == "RandomContrast":
                cfg["config"].pop("value_range", None)
            for key in cfg:
                remove_data_format(cfg[key])
        elif isinstance(cfg, list):
            for item in cfg:
                remove_data_format(item)

    remove_data_format(config_dict)

    # Overwrite with cleaned config
    f.attrs["model_config"] = json.dumps(config_dict).encode("utf-8")