#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
画像ファイルをXOR暗号化してBase64エンコードするスクリプト
"""
import base64
import os
import json

def xor_encrypt(data, key):
    """XOR暗号化"""
    key_bytes = key.encode('utf-8')
    key_len = len(key_bytes)
    encrypted = bytearray()
    
    for i, byte in enumerate(data):
        encrypted.append(byte ^ key_bytes[i % key_len])
    
    return bytes(encrypted)

def encrypt_image(input_file, output_file, password):
    """画像ファイルを暗号化"""
    print(f"読み込み中: {input_file}")
    
    # 画像ファイルを読み込む
    with open(input_file, 'rb') as f:
        image_data = f.read()
    
    print(f"ファイルサイズ: {len(image_data)} bytes")
    
    # XOR暗号化
    print("暗号化中...")
    encrypted_data = xor_encrypt(image_data, password)
    
    # Base64エンコード
    print("Base64エンコード中...")
    base64_data = base64.b64encode(encrypted_data).decode('utf-8')
    
    # ファイルに保存
    print(f"保存中: {output_file}")
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(base64_data)
    
    print(f"完了！暗号化後のサイズ: {len(base64_data)} bytes")

def encrypt_photos_folder(photos_dir, password):
    """photosフォルダ内の全画像を暗号化"""
    photo_files = []
    counter = 1
    
    for filename in os.listdir(photos_dir):
        if filename.lower().endswith(('.jpg', '.jpeg', '.png', '.gif')):
            input_path = os.path.join(photos_dir, filename)
            
            # 難読化したファイル名を生成
            encrypted_filename = f"p{counter:03d}.enc"
            output_path = os.path.join(photos_dir, encrypted_filename)
            
            print(f"\n[{counter}] {filename}")
            encrypt_image(input_path, output_path, password)
            
            photo_files.append({
                'id': counter,
                'original': filename,
                'encrypted': encrypted_filename,
                'title': f"写真{counter}"
            })
            
            counter += 1
    
    # マッピング情報をJSONで保存
    mapping_file = os.path.join(photos_dir, 'photos_mapping.json')
    with open(mapping_file, 'w', encoding='utf-8') as f:
        json.dump(photo_files, f, ensure_ascii=False, indent=2)
    
    print(f"\n✅ {len(photo_files)}枚の写真を暗号化しました")
    print(f"マッピング情報: {mapping_file}")
    
    return photo_files

if __name__ == "__main__":
    photos_dir = "docs/groupinfo/photos"
    password = "ohtoshi2026"
    
    if not os.path.exists(photos_dir):
        print(f"エラー: フォルダが見つかりません: {photos_dir}")
        exit(1)
    
    photo_files = encrypt_photos_folder(photos_dir, password)
    
    print("\n元の画像ファイルは手動で削除してください:")
    for photo in photo_files:
        print(f"  - {photo['original']}")
