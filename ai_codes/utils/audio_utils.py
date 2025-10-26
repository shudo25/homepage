import speech_recognition as sr

def get_device_index_by_name(target_names):
    """
    デバイス名リストから部分一致でインデックスを返す。見つからなければRuntimeError。
    :param target_names: 検索したいデバイス名のリスト（部分一致）
    :return: インデックス番号
    """
    devices = sr.Microphone.list_microphone_names()
    for i, name in enumerate(devices):
        for target in target_names:
            if target in name:
                return i
    raise RuntimeError(f"対象デバイスが見つかりません: {target_names}")
