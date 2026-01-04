#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PDFファイルをXOR暗号化してBase64エンコードするスクリプト
"""
import base64
import sys
import os

def xor_encrypt(data, key):
    """XOR暗号化"""
    key_bytes = key.encode('utf-8')
    key_len = len(key_bytes)
    encrypted = bytearray()
    
    for i, byte in enumerate(data):
        encrypted.append(byte ^ key_bytes[i % key_len])
    
    return bytes(encrypted)

def encrypt_pdf(input_file, output_file, password):
    """PDFファイルを暗号化"""
    print(f"読み込み中: {input_file}")
    
    # PDFファイルを読み込む
    with open(input_file, 'rb') as f:
        pdf_data = f.read()
    
    print(f"ファイルサイズ: {len(pdf_data)} bytes")
    
    # XOR暗号化
    print("暗号化中...")
    encrypted_data = xor_encrypt(pdf_data, password)
    
    # Base64エンコード
    print("Base64エンコード中...")
    base64_data = base64.b64encode(encrypted_data).decode('utf-8')
    
    # ファイルに保存
    print(f"保存中: {output_file}")
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(base64_data)
    
    print(f"完了！暗号化後のサイズ: {len(base64_data)} bytes")
    print(f"サイズ増加率: {len(base64_data) / len(pdf_data) * 100:.1f}%")

if __name__ == "__main__":
    input_pdf = "docs/groupinfo/d8f3a7c9b5e2f1a4d6c8b9e7f3a5c2d1.pdf"
    output_file = "docs/groupinfo/d8f3a7c9b5e2f1a4d6c8b9e7f3a5c2d1.enc"
    password = "ohtoshi2026"
    
    if not os.path.exists(input_pdf):
        print(f"エラー: ファイルが見つかりません: {input_pdf}")
        sys.exit(1)
    
    encrypt_pdf(input_pdf, output_file, password)
    print("\n✅ 暗号化が完了しました")
    print(f"元のPDFファイル（{input_pdf}）は手動で削除してください")
