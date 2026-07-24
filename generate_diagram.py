# -*- coding: utf-8 -*-
"""
Script to generate Current-State Workflow diagram for Vinmec Discharge Summary
Run: python generate_diagram.py
Output: 04-workflow-diagram.png
"""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import numpy as np

fig, ax = plt.subplots(1, 1, figsize=(18, 11))
ax.set_xlim(0, 18)
ax.set_ylim(0, 11)
ax.axis('off')

# ─── Colors ─────────────────────────────────────────────────────────────────
COLOR_HEADER    = '#1a1a2e'
COLOR_STEP      = '#16213e'
COLOR_BOTTLENECK= '#c0392b'
COLOR_HANDOFF   = '#2980b9'
COLOR_NORMAL    = '#2d6a4f'
COLOR_ACCENT    = '#f39c12'
COLOR_BG        = '#0f3460'
COLOR_LIGHT     = '#e8f4f8'
COLOR_TEXT      = '#ffffff'
COLOR_SUBTEXT   = '#b0c4de'
COLOR_ARROW     = '#e74c3c'

fig.patch.set_facecolor('#0d1b2a')
ax.set_facecolor('#0d1b2a')

# ─── Title & header ─────────────────────────────────────────────────────────
ax.text(9, 10.4, 'CURRENT-STATE WORKFLOW — Quy Trình Soạn Discharge Summary',
        ha='center', va='center', fontsize=15, fontweight='bold',
        color='white', fontfamily='monospace')
ax.text(9, 9.95, 'Vinmec Hospital · Khoa Nội Trú · Vin Smart Future — Lab 02',
        ha='center', va='center', fontsize=10,
        color='#7fb3d3')

# Draw separator line
ax.plot([0.5, 17.5], [9.7, 9.7], color='#2980b9', linewidth=1.5, alpha=0.7)

# ─── Helper: draw step box ───────────────────────────────────────────────────
def draw_step(ax, x, y, w, h, step_num, title, actor, time_str,
              input_str, output_str, color=COLOR_STEP, is_bottleneck=False):
    # Outer glow for bottleneck
    if is_bottleneck:
        glow = FancyBboxPatch((x - 0.07, y - 0.07), w + 0.14, h + 0.14,
                               boxstyle="round,pad=0.05",
                               linewidth=3, edgecolor='#e74c3c',
                               facecolor='none', alpha=0.7, zorder=2)
        ax.add_patch(glow)

    box = FancyBboxPatch((x, y), w, h,
                          boxstyle="round,pad=0.12",
                          linewidth=1.5 if not is_bottleneck else 2.5,
                          edgecolor='#e74c3c' if is_bottleneck else '#34495e',
                          facecolor=color, zorder=3)
    ax.add_patch(box)

    # Step label
    badge_color = '#e74c3c' if is_bottleneck else '#2980b9'
    badge = FancyBboxPatch((x + 0.08, y + h - 0.45), 1.05, 0.35,
                            boxstyle="round,pad=0.05",
                            linewidth=0, facecolor=badge_color, zorder=4)
    ax.add_patch(badge)
    ax.text(x + 0.6, y + h - 0.28, step_num,
            ha='center', va='center', fontsize=8, fontweight='bold',
            color='white', zorder=5)

    # Bottleneck label
    if is_bottleneck:
        ax.text(x + w - 0.15, y + h - 0.22, '🔴 BOTTLENECK',
                ha='right', va='center', fontsize=6.5, fontweight='bold',
                color='#e74c3c', zorder=5)

    # Title
    ax.text(x + w / 2, y + h - 0.68, title,
            ha='center', va='center', fontsize=9.5, fontweight='bold',
            color='white', zorder=5, wrap=True)

    # Divider
    ax.plot([x + 0.15, x + w - 0.15], [y + h - 0.85, y + h - 0.85],
            color='#34495e', linewidth=0.8, zorder=5)

    # Actor
    ax.text(x + 0.2, y + h - 1.08, f'Actor: {actor}',
            ha='left', va='center', fontsize=7.5, color='#7fb3d3', zorder=5)

    # Time
    t_color = '#e74c3c' if is_bottleneck else '#2ecc71'
    ax.text(x + 0.2, y + h - 1.38, f'Time: {time_str}',
            ha='left', va='center', fontsize=8, fontweight='bold',
            color=t_color, zorder=5)

    # Input / Output
    ax.text(x + 0.2, y + h - 1.68, f'IN:  {input_str}',
            ha='left', va='center', fontsize=7, color=COLOR_SUBTEXT, zorder=5)
    ax.text(x + 0.2, y + h - 1.98, f'OUT: {output_str}',
            ha='left', va='center', fontsize=7, color=COLOR_SUBTEXT, zorder=5)


# ─── Step boxes (y top-row ~7.8, height=2.6) ────────────────────────────────
BOX_H = 2.55
ROW_Y = 5.2   # bottom of boxes in top row

steps_top = [
    dict(x=0.5,  y=ROW_Y, w=3.2, h=BOX_H,
         step_num='BƯỚC 1', title='Mở bệnh án\nHIS Vinmec',
         actor='Bác sĩ điều trị', time_str='~2 phút',
         input_str='Chỉ định xuất viện', output_str='HIS session mở',
         is_bottleneck=False),
    dict(x=4.2,  y=ROW_Y, w=3.2, h=BOX_H,
         step_num='BƯỚC 2', title='Đọc thủ công\nbệnh án & XN',
         actor='Bác sĩ điều trị', time_str='~10 phút 🔴',
         input_str='Ghi chú, XN, CĐHA', output_str='Ghi nhớ tổng hợp',
         is_bottleneck=True),
    dict(x=7.9,  y=ROW_Y, w=3.2, h=BOX_H,
         step_num='BƯỚC 3', title='Soạn thủ công\nDischarge Summary',
         actor='Bác sĩ điều trị', time_str='~15 phút 🔴',
         input_str='Thông tin từ bộ nhớ', output_str='Draft Word/Form',
         is_bottleneck=True),
    dict(x=11.6, y=ROW_Y, w=3.2, h=BOX_H,
         step_num='BƯỚC 4', title='Ký tên & đóng\ndấu xác nhận',
         actor='Bác sĩ điều trị', time_str='~2 phút',
         input_str='Bản draft đã soạn', output_str='Tài liệu có chữ ký',
         is_bottleneck=False),
    dict(x=15.3, y=ROW_Y, w=2.2, h=BOX_H,
         step_num='BƯỚC 5', title='Trao cho\nbệnh nhân',
         actor='Điều dưỡng', time_str='~2 phút',
         input_str='Tài liệu in', output_str='Bệnh nhân nhận',
         is_bottleneck=False),
]

for s in steps_top:
    draw_step(ax, **s)

# ─── Arrows between boxes ────────────────────────────────────────────────────
arrow_props = dict(arrowstyle='->', color='#5dade2',
                   lw=2, mutation_scale=18)

connects = [
    (3.70, 6.53, 4.20, 6.53),
    (7.40, 6.53, 7.90, 6.53),
    (11.10, 6.53, 11.60, 6.53),
    (14.80, 6.53, 15.30, 6.53),
]
for x1, y1, x2, y2 in connects:
    ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                arrowprops=arrow_props, zorder=6)

# Handoff labels on arrows
handoff_positions = [(3.95, 6.75), (7.65, 6.75), (11.35, 6.75), (15.05, 6.75)]
for hx, hy in handoff_positions:
    ax.text(hx, hy, '[Handoff]', ha='center', va='center', fontsize=6.5,
            color='#5dade2', fontweight='bold', zorder=7)

# ─── Time summary bar ────────────────────────────────────────────────────────
bar_y = 4.6
ax.add_patch(FancyBboxPatch((0.5, bar_y - 0.4), 17, 0.75,
                              boxstyle="round,pad=0.1",
                              linewidth=1.5, edgecolor='#c0392b',
                              facecolor='#1c0a0a', zorder=3))

segments = [
    (0.5,  2.0, '#2ecc71', 'Bước 1\n2 min'),
    (2.9,  5.3, '#e74c3c', 'Bước 2\n10 min 🔴'),
    (8.7,  5.3, '#c0392b', 'Bước 3\n15 min 🔴'),
    (14.5, 1.8, '#2ecc71', 'Bước 4\n2 min'),
    (16.7, 0.8, '#27ae60', 'B5\n2m'),
]
bar_fill_y = bar_y - 0.3
bar_h = 0.55
cur_x = 0.7
total_min = 31
px_total = 16.6

for seg_start, seg_min, col, label in segments:
    seg_w = (seg_min / total_min) * px_total
    ax.add_patch(FancyBboxPatch((cur_x, bar_fill_y), seg_w, bar_h * 0.7,
                                  boxstyle="square,pad=0",
                                  linewidth=0, facecolor=col,
                                  alpha=0.85, zorder=4))
    ax.text(cur_x + seg_w / 2, bar_fill_y + bar_h * 0.35,
            label, ha='center', va='center', fontsize=6.5,
            color='white', fontweight='bold', zorder=5)
    cur_x += seg_w

ax.text(0.7, bar_y + 0.55, 'Phan bo thoi gian theo tung buoc:',
        ha='left', va='center', fontsize=8, color='#7fb3d3')
ax.text(17.3, bar_y + 0.55, 'TONG: ~31 phut/benh nhan',
        ha='right', va='center', fontsize=9, fontweight='bold', color='#e74c3c')

# ─── Legend ──────────────────────────────────────────────────────────────────
leg_y = 3.7
ax.text(0.7, leg_y, 'Chú giải:', ha='left', va='center',
        fontsize=9, fontweight='bold', color='white')

legend_items = [
    ('#e74c3c', '[BOTTLENECK] Buoc gay tac nghen, chiem phan lon thoi gian'),
    ('#2980b9', '[HANDOFF] Diem chuyen giao thong tin giua nguoi/he thong'),
    ('#2ecc71', '[NORMAL] Buoc binh thuong, thoi gian ngan'),
]
for i, (color, text) in enumerate(legend_items):
    lx = 0.7 + i * 5.9
    ax.add_patch(FancyBboxPatch((lx, leg_y - 0.55), 0.35, 0.35,
                                  boxstyle="round,pad=0.05",
                                  linewidth=0, facecolor=color, zorder=5))
    ax.text(lx + 0.5, leg_y - 0.38, text,
            ha='left', va='center', fontsize=7.8, color='#b0c4de', zorder=5)

# ─── Bottom key metrics ──────────────────────────────────────────────────────
metrics = [
    ('Benh nhan/ngay', '150-300 ca\n(toan benh vien)', '#3498db'),
    ('Tong thoi gian/ca', '~31 phut\n(thu cong)', '#e74c3c'),
    ('BOTTLENECK chinh', 'Buoc 2+3\n25 phut (80%)', '#c0392b'),
    ('Chi phi co hoi', '62-125 gio bac si/ngay\n~31-100M VND/ngay', '#e67e22'),
    ('Muc tieu AI', 'Giam con < 5 phut/ca\n(giam 80%)', '#2ecc71'),
]
metric_box_y = 0.3
box_w = 3.2
for i, (label, val, col) in enumerate(metrics):
    mx = 0.5 + i * (box_w + 0.15)
    ax.add_patch(FancyBboxPatch((mx, metric_box_y), box_w, 2.2,
                                  boxstyle="round,pad=0.12",
                                  linewidth=1.5, edgecolor=col,
                                  facecolor='#0d1b2a', alpha=0.9, zorder=3))
    ax.text(mx + box_w / 2, metric_box_y + 1.5, label,
            ha='center', va='center', fontsize=8, color='#7fb3d3',
            fontweight='bold', zorder=5)
    ax.text(mx + box_w / 2, metric_box_y + 0.65, val,
            ha='center', va='center', fontsize=9, color=col,
            fontweight='bold', zorder=5)

plt.tight_layout(pad=0.5)
plt.savefig('04-workflow-diagram.png', dpi=150, bbox_inches='tight',
            facecolor='#0d1b2a', edgecolor='none')
print("[OK] Da tao file 04-workflow-diagram.png thanh cong!")
plt.close()
