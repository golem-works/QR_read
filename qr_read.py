import sys
sys.path.append("./QR-Code-generator/python")  # ← 最初にパス追加！

import os
import ezdxf
import tkinter as tk
from tkinter import messagebox
from qrcodegen import *
import matplotlib.pyplot as plt
from ezdxf.addons.drawing import RenderContext, Frontend
from ezdxf.addons.drawing.matplotlib import MatplotlibBackend


def generate_qr_dxf(text):
    if not text:
        messagebox.showwarning("⚠ 入力エラー", "QRコードの内容を入力してください")
        return

    doc = ezdxf.new("R2018", setup=True)
    msp = doc.modelspace()
    qr = QrCode.encode_text(text, QrCode.Ecc.MEDIUM)

    for y in range(qr.get_size()):
        for x in range(qr.get_size()):
            if qr.get_module(x, y):
                poly = msp.add_lwpolyline(
                    [
                        (x, qr.get_size() - y - 1),
                        (x + 1, qr.get_size() - y - 1),
                        (x + 1, qr.get_size() - y),
                        (x, qr.get_size() - y),
                        (x, qr.get_size() - y - 1),
                    ],
                    close=True,
                )
                hatch = msp.add_hatch()
                hatch.paths.add_polyline_path(poly.get_points(format="xyb"), is_closed=True)

    safe_name = "".join(c for c in text[:10] if c.isalnum()) or "qrcode"
    dxf_file = f"{safe_name}.dxf"

    doc.saveas(dxf_file)
    messagebox.showinfo("✅ 完了", f"DXFファイルを保存しました：{dxf_file}")

    fig = plt.figure()
    ax = fig.add_axes([0, 0, 1, 1])
    ctx = RenderContext(doc)
    out = MatplotlibBackend(ax)
    Frontend(ctx, out).draw_layout(msp, finalize=True)
    plt.show()


# GUI setup
root = tk.Tk()
root.title("QRコード → DXF 変換ツール")
root.geometry("420x160")

label = tk.Label(root, text="📩 QRコードに埋め込む文字列を入力してください：")
label.pack(pady=5)

entry = tk.Entry(root, width=50)
entry.pack(pady=5)

btn = tk.Button(root, text="QRコードを生成して保存", command=lambda: generate_qr_dxf(entry.get()))
btn.pack(pady=15)

root.mainloop()
