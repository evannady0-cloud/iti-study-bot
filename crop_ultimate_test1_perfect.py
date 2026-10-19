import pymupdf
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

pdf_path = r'C:\Users\tonyn\Desktop\ITI_Preparation_Material\IQ\Ultimate_IQ_Tests_كتاب_ألتيمت.pdf'
doc = pymupdf.open(pdf_path)

out_dirs = [
    r'C:\Users\tonyn\.gemini\antigravity\scratch\iti_telegram_bot\crops',
    r'C:\Users\tonyn\.gemini\antigravity\scratch\iti_telegram_bot\images'
]

# Exact bounding boxes for each visual question in Test 1
# format: (q_num, page_index_0_based, y_top, y_bottom, x_left, x_right)
# Page width is ~482, page height is ~680.
crops_config = [
    (1,  7,  260, 620, 40, 442),  # Q1: Square completion with pieces A-E
    (6,  8,  220, 540, 40, 442),  # Q6: Missing section in number grid
    (7,  9,  45,  355, 40, 442),  # Q7: Odd one out among diagrams A-E
    (9,  9,  435, 615, 40, 442),  # Q9: Number pyramid
    (10, 10, 45,  250, 40, 442),  # Q10: Odd one out rotated shapes A-E
    (14, 11, 45,  325, 40, 442),  # Q14: Circuit diagram with switches 1-4
    (15, 11, 328, 560, 40, 442),  # Q15: 3x3 rings matrix
    (18, 12, 155, 250, 40, 442),  # Q18: Segment circles with numbers
    (20, 12, 380, 615, 40, 442),  # Q20: How many straight lines appear (FULL diagram without cuts!)
    (21, 13, 45,  325, 40, 442),  # Q21: 3x3 arrows grid
    (23, 13, 370, 610, 40, 442),  # Q23: Letter grid
    (31, 14, 508, 590, 40, 442),  # Q31: Sequence of circles with dots
    (36, 15, 198, 620, 40, 442),  # Q36: Hexagon with dots A-E
    (37, 16, 45,  310, 40, 442),  # Q37: Word letter trace diagram
    (38, 16, 320, 610, 40, 442),  # Q38: Letter hex wheel
    (39, 17, 45,  210, 40, 442),  # Q39: Multiplication grid
    (40, 17, 210, 610, 40, 442),  # Q40: Corner blocks missing section
]

for q_num, p_idx, y0, y1, x0, x1 in crops_config:
    page = doc[p_idx]
    rect = pymupdf.Rect(x0, y0, x1, y1)
    # Render at high resolution 200 DPI
    pix = page.get_pixmap(dpi=200, clip=rect)
    
    file_names = [
        f'ultimate_test1_q{q_num:02d}.png',
        f'ultimate_test1_q{q_num}.png'
    ]
    
    for d in out_dirs:
        for fname in file_names:
            out_path = os.path.join(d, fname)
            pix.save(out_path)
            
    print(f"Rendered Q{q_num:02d} (p{p_idx+1}): size=({pix.width}x{pix.height}) y=[{y0}-{y1}]")

print("All 17 Ultimate IQ Test 1 visual questions cropped perfectly!")
