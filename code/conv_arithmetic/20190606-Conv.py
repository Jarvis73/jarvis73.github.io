import itertools
import os
import subprocess
from glob import glob
from pathlib import Path

import numpy as np
import six

np.random.seed(1234)


def make_numerical_tex_string(step, input_size, output_size,
                              kernel_size, transposed=False):
    # Used to add bottom-padding to account for odd shapes
    bottom_pad = input_size - kernel_size

    x0 = 0
    k = kernel_size
    if transposed:
        fi = output_size
        fip = output_size + (k - 1) * 2
        fo = input_size
        kvi = list(range(k - 1, -1, -1))
        kvj = list(range(k))
        ivv = "b"
        ovv = "a"
        ivi = list(range(fi))
        ivj = list(range(fi - 1, -1, -1))
        ovi = list(range(fo))
        ovj = list(range(fo - 1, -1, -1))
        p = k - 1
    else:
        fi = input_size
        fip = input_size
        fo = output_size
        kvi = list(range(k))
        kvj = list(range(k - 1, -1, -1))
        ivv = "a"
        ovv = "b"
        ivi = list(range(fi))
        ivj = list(range(fi - 1, -1, -1))
        ovi = list(range(fo))
        ovj = list(range(fo - 1, -1, -1))
        p = 0
    mw = input_size ** 2
    mh = output_size ** 2
    max_steps = fo ** 2

    if mh > fip + fo + 2:
        y0 = (mh - (fip + fo + 2)) // 2
        y2 = 0
        half_cut_h = (mh - 2) // 2
        total_h = mh
        y3 = 0
        y4 = 0
    else:
        y0 = 0
        y2 = ((fip + fo + 2) - mh) // 2
        half_cut_h = (fip + fo) // 2
        total_h = fip + fo + 2
        y3 = y2 if transposed else 0
        y4 = 0 if transposed else y2
    head = half_cut_h
    tail = total_h - 2 - half_cut_h
    
    if step >= max_steps:
        raise ValueError(
            'step {} out of bounds (there are {} steps for this animation'.format(step, max_steps))

    offsets = list(itertools.product(range(fo - 1, -1, -1), range(fo)))
    offset_y, offset_x = offsets[step]

    klv = np.zeros((mh, mw), dtype=np.uint8)    # kernel flat values
    for x in range(mh):
        steps_per_row = input_size - k + 1
        zeros = np.zeros((input_size, input_size), dtype=np.uint8)
        ofx, ofy = x // steps_per_row, x % steps_per_row
        zeros[ofx:ofx + k, ofy:ofy+k] = 1
        klv[x] = zeros.reshape(-1)
    klvx = [np.where(line == 1)[0] for line in klv]
    klvy = [np.where(line == 1)[0] for line in klv.T]

    if transposed:
        kernel_flat_string = ''.join(
            ["\\draw[step=10mm, base03, thick] ({},0) grid ({},{});\n".format(step, step + 1, mh)
        ] + ["\\draw[fill=blue] ({0},{1}) rectangle ({2},{3});\n\\draw[fill=base02, opacity=0.4] ({0},{1}) rectangle ({2},{3});\n".format(step, mh - y - 1, step + 1, mh - y) for y in klvy[step]
        ])
    else:
        kernel_flat_string = ''.join(
            ["\\draw[step=10mm, base03, thick] (0,{}) grid ({},{});\n".format(mh - step - 1, mw, mh - step)
        ] + ["\\draw[fill=blue] ({0},{1}) rectangle ({2},{3});\n\\draw[fill=base02, opacity=0.4] ({0},{1}) rectangle ({2},{3});\n".format(x, mh - step - 1, x + 1, mh - step) for x in klvx[step]
        ])
    kernel_flat_string += ''.join(
        ["\\node (node) at ({},{}) {{\\large $ w_{{{}{}}} $}};\n".format(x + 0.5, mh - y - 0.5, ix, iy)
         for y in range(mh) for x, (ix, iy) in zip(klvx[y], itertools.product(range(k), range(k)))
    ])

    def gen_head_tail(lst, head, tail):
        lst = list(lst)
        for y, (ix, iy) in lst[:tail]:
            yield y - (mw - total_h), ix, iy
        for y, (ix, iy) in lst[-head:]:
            yield y, ix, iy

    if transposed:
        input_flat_string = ''.join(
            ["\\draw[fill=cyan] (0,0) rectangle (1,{});\n".format(mh),
             "\\draw[step=10mm, base03, thick] (0,0) grid (1,{});\n".format(mh),
        ] + ["\\node (node) at (0.5, {}) {{\large $ b_{{{}{}}} $}};\n".format(y + 0.5, ix, iy)
            for y, (ix, iy) in zip(range(mh - 1, -1, -1), itertools.product(range(fi), range(fi)))
        ])

        output_flat_string = ''.join(
            ["\\draw[fill=blue] (0,0) rectangle (1,{});\n".format(half_cut_h),
             "\\draw[fill=blue] (0,{}) rectangle (1,{});\n".format(half_cut_h + 2, total_h),
        ] + ["\\draw[step=10mm, base03, thick] (0,0) grid (1,{});\n".format(half_cut_h),
             "\\draw[step=10mm, base03, thick] (0,{}) grid (1,{});\n".format(half_cut_h + 2, total_h),
        ] + [
            "\\node (node) at (0.5, {} + 0.6) {{\large $ \\vdots $}};\n".format(half_cut_h),
            "\\node (node) at (0.5, {} + 1.6) {{\large $ \\vdots $}};\n".format(half_cut_h)
        ])
        if step < tail:
            output_flat_string += ''.join(
                ["\\draw[fill=base02, opacity=0.4] (0,{}) rectangle (1,{});\n".format(total_h - step - 1, total_h - step),
            ])
        elif step > mw - head - 1:
            diff = step - (mw - head - 1)
            output_flat_string += ''.join(
                ["\\draw[fill=base02, opacity=0.4] (0,{}) rectangle (1,{});\n".format(head - diff, head - diff + 1),
            ])
        output_flat_string += ''.join(
            ["\\node (node) at (0.5, {}) {{\large $ a_{{{}{}}} $}};\n".format(y + 0.5, ix, iy)
                for y, ix, iy in gen_head_tail(zip(range(mw - 1, -1, -1), itertools.product(range(fo), range(fo))), head, tail)
            ])
    else:
        input_flat_string = ''.join(
            ["\\draw[fill=blue] (0,0) rectangle (1,{});\n".format(half_cut_h),
             "\\draw[fill=blue] (0,{}) rectangle (1,{});\n".format(half_cut_h + 2, total_h),
        ] + ["\\draw[step=10mm, base03, thick] (0,0) grid (1,{});\n".format(half_cut_h),
             "\\draw[step=10mm, base03, thick] (0,{}) grid (1,{});\n".format(half_cut_h + 2, total_h),
        ] + ["\\node (node) at (0.5, {}) {{\large $ a_{{{}{}}} $}};\n".format(y + 0.5, ix, iy)
            for y, ix, iy in gen_head_tail(
                zip(range(mw - 1, -1, -1), itertools.product(range(fip), range(fip))), head, tail)
        ] + [
            "\\node (node) at (0.5, {} + 0.6) {{\large $ \\vdots $}};\n".format(half_cut_h),
            "\\node (node) at (0.5, {} + 1.6) {{\large $ \\vdots $}};\n".format(half_cut_h)
        ])

        output_flat_string = ''.join(
            ["\\draw[fill=cyan] (0,0) rectangle (1,{});\n".format(mh),
        ] + ["\\draw[step=10mm, base03, thick] (0,0) grid (1,{});\n".format(mh),
             "\\draw[fill=base02, opacity=0.4] (0,{}) rectangle (1,{});\n".format(mh - step - 1, mh - step),
        ] + ["\\node (node) at (0.5, {}) {{\large $ b_{{{}{}}} $}};\n".format(y + 0.5, ix, iy)
            for y, (ix, iy) in zip(range(mh - 1, -1, -1), itertools.product(range(fo), range(fo)))
        ])

    openfile = '20190606-numerical-transpose.txt' if transposed else '20190606-numerical.txt'
    with open(openfile, 'r') as f:
        tex_template = f.read()

    return six.b(tex_template.format(**{
        'XSHIFT0': '{}'.format(x0),
        'YSHIFT0': '{}'.format(y0),
        'PADDING_TO': '{0},{0}'.format(fip),
        'INPUT_FROM': '{0},{0}'.format(p),
        'INPUT_TO': '{0},{0}'.format(fip - p),
        'INPUT_VALUES': ''.join(
            "\\node (node) at ({0},{1}) {{\\large $ {4}_{{{2}{3}}} $}};\n".format(
                i + 0.4 + p, j + 0.6 + p, ivj[j], ivi[i], ivv)
            for i, j in itertools.product(range(fi), range(fi))),
        'INPUT_GRID_FROM': '{},{}'.format(offset_x, offset_y),
        'INPUT_GRID_TO': '{},{}'.format(offset_x + k, offset_y + k),
        'KERNEL_VALUES': ''.join(
            "\\node (node) at ({0},{1}) {{\\scriptsize $ w_{{{2}{3}}} $}};\n".format(
                i + 0.75 + offset_x, j + 0.2 + offset_y, kvj[j], kvi[i])
            for i, j in itertools.product(range(k), range(k))),
        'OUTPUT_TO': '{0},{0}'.format(fo),
        'OUTPUT_GRID_FROM': '{},{}'.format(offset_x, offset_y),
        'OUTPUT_GRID_TO': '{},{}'.format(offset_x + 1, offset_y + 1),
        'OUTPUT_VALUES': ''.join(
            "\\node (node) at ({0},{1}) {{\\large $ {4}_{{{2}{3}}} $}};\n".format(
                i + 0.5, j + 0.5, ovj[j], ovi[i], ovv)
            for i, j in itertools.product(range(fo), range(fo))),
        'XSHIFT1': '{}'.format(x0 + (fip - fo) // 2),
        'YSHIFT1': '{}'.format(y0 + fip + 2),
        'XSHIFT2': '{}'.format(x0 + fip + 2),
        'YSHIFT2': '{}'.format(y2),
        'FLAT_TO_X': '{}'.format(mw),
        'FLAT_TO_Y': '{}'.format(mh),
        'XSHIFT3': '{}'.format(x0 + fip + 2 + mw + 2),
        'YSHIFT3': '{}'.format(y3),
        'YSHIFT4': '{}'.format(y4),
        'HALF_CUT_H': '{}'.format(half_cut_h),
        'TOTAL_H': '{}'.format(total_h),
        'KERNEL_FLAT_VALUES': kernel_flat_string,
        'INPUT_FLAT_VALUES': input_flat_string,
        'OUTPUT_FLAT_VALUES': output_flat_string,
    }))

def make_numerical_tex_string_conv_v2(step, input_size, output_size, kernel_size):
    """
    Exchange the meaning of 'kernel' and 'input' in this function for convenience.
    """

    # Used to add bottom-padding to account for odd shapes
    bottom_pad = input_size - kernel_size

    x0 = 0
    k = kernel_size
    fi = input_size
    fip = input_size
    fo = output_size
    kvi = list(range(k))
    kvj = list(range(k - 1, -1, -1))
    ivv = "a"
    ovv = "b"
    ivi = list(range(fi))
    ivj = list(range(fi - 1, -1, -1))
    ovi = list(range(fo))
    ovj = list(range(fo - 1, -1, -1))
    p = 0
    mw = kernel_size ** 2
    mh = output_size ** 2
    max_steps = fo ** 2

    if mh > fip + fo + 2:
        y0 = (mh - (fip + fo + 2)) // 2
        y2 = 0
        half_cut_h = (mh - 2) // 2
        total_h = mh
        y3 = 0
        y4 = 0
    else:
        y0 = 0
        y2 = ((fip + fo + 2) - mh) // 2
        half_cut_h = (fip + fo) // 2
        total_h = fip + fo + 2
        y3 = 0
        y4 = y2
    head = half_cut_h
    tail = total_h - 2 - half_cut_h
    
    if step >= max_steps:
        raise ValueError(
            'step {} out of bounds (there are {} steps for this animation'.format(step, max_steps))

    offsets = list(itertools.product(range(fo - 1, -1, -1), range(fo)))
    offset_y, offset_x = offsets[step]

    klv = np.ones((mh, mw), dtype=np.uint8)    # kernel flat values
    klvx = [np.where(line == 1)[0] for line in klv]
    klvy = [np.where(line == 1)[0] for line in klv.T]

    kernel_flat_string = ''.join(
        ["\\draw[step=10mm, base03, thick] (0,{}) grid ({},{});\n".format(mh - step - 1, mw, mh - step)
    ] + ["\\draw[fill=blue] ({0},{1}) rectangle ({2},{3});\n".format(x, mh - step - 1, x + 1, mh - step) for x in klvx[step]
    ])
    kernel_flat_string += ''.join(
        ["\\node (node) at ({},{}) {{\\large $ a_{{{}{}}} $}};\n".format(x + 0.5, mh - y - 0.5, ix + y // k, iy + y % k)
         for y in range(mh) for x, (ix, iy) in zip(klvx[y], itertools.product(range(k), range(k)))
    ])

    def gen_head_tail(lst, head, tail):
        lst = list(lst)
        for y, (ix, iy) in lst[:tail]:
            yield y - (mw - total_h), ix, iy
        for y, (ix, iy) in lst[-head:]:
            yield y, ix, iy

    input_flat_string = ''.join(
        ["\\draw[fill=blue] (0,0) rectangle (1,{0});\n\\draw[fill=base02, opacity=0.4] (0,0) rectangle (1,{0});\n".format(mh),
            "\\draw[step=10mm, base03, thick] (0,0) grid (1,{});\n".format(mh),
    ] + ["\\node (node) at (0.5, {}) {{\large $ w_{{{}{}}} $}};\n".format(y + 0.5, ix, iy)
        for y, (ix, iy) in zip(range(mh - 1, -1, -1), itertools.product(range(fi), range(fi)))
    ])

    output_flat_string = ''.join(
        ["\\draw[fill=cyan] (0,0) rectangle (1,{});\n".format(mh),
    ] + ["\\draw[step=10mm, base03, thick] (0,0) grid (1,{});\n".format(mh),
            "\\draw[fill=base02, opacity=0.4] (0,{}) rectangle (1,{});\n".format(mh - step - 1, mh - step),
    ] + ["\\node (node) at (0.5, {}) {{\large $ b_{{{}{}}} $}};\n".format(y + 0.5, ix, iy)
        for y, (ix, iy) in zip(range(mh - 1, -1, -1), itertools.product(range(fo), range(fo)))
    ])

    with open('20190606-numerical-conv-v2.txt', 'r') as f:
        tex_template = f.read()

    return six.b(tex_template.format(**{
        'XSHIFT0': '{}'.format(x0),
        'YSHIFT0': '{}'.format(y0),
        'PADDING_TO': '{0},{0}'.format(fip),
        'INPUT_FROM': '{0},{0}'.format(p),
        'INPUT_TO': '{0},{0}'.format(fip - p),
        'INPUT_VALUES': ''.join(
            "\\node (node) at ({0},{1}) {{\\large $ {4}_{{{2}{3}}} $}};\n".format(
                i + 0.4 + p, j + 0.6 + p, ivj[j], ivi[i], ivv)
            for i, j in itertools.product(range(fi), range(fi))),
        'INPUT_GRID_FROM': '{},{}'.format(offset_x, offset_y),
        'INPUT_GRID_TO': '{},{}'.format(offset_x + k, offset_y + k),
        'KERNEL_VALUES': ''.join(
            "\\node (node) at ({0},{1}) {{\\scriptsize $ w_{{{2}{3}}} $}};\n".format(
                i + 0.75 + offset_x, j + 0.2 + offset_y, kvj[j], kvi[i])
            for i, j in itertools.product(range(k), range(k))),
        'OUTPUT_TO': '{0},{0}'.format(fo),
        'OUTPUT_GRID_FROM': '{},{}'.format(offset_x, offset_y),
        'OUTPUT_GRID_TO': '{},{}'.format(offset_x + 1, offset_y + 1),
        'OUTPUT_VALUES': ''.join(
            "\\node (node) at ({0},{1}) {{\\large $ {4}_{{{2}{3}}} $}};\n".format(
                i + 0.5, j + 0.5, ovj[j], ovi[i], ovv)
            for i, j in itertools.product(range(fo), range(fo))),
        'XSHIFT1': '{}'.format(x0 + (fip - fo) // 2),
        'YSHIFT1': '{}'.format(y0 + fip + 2),
        'XSHIFT2': '{}'.format(x0 + fip + 2),
        'YSHIFT2': '{}'.format(y2),
        'FLAT_TO_X': '{}'.format(mw),
        'FLAT_TO_Y': '{}'.format(mh),
        'XSHIFT3': '{}'.format(x0 + fip + 2 + mw + 2),
        'YSHIFT3': '{}'.format(y3),
        'YSHIFT4': '{}'.format(y4),
        'HALF_CUT_H': '{}'.format(half_cut_h),
        'TOTAL_H': '{}'.format(total_h),
        'KERNEL_FLAT_VALUES': kernel_flat_string,
        'INPUT_FLAT_VALUES': input_flat_string,
        'OUTPUT_FLAT_VALUES': output_flat_string,
    }))

def compile_figure(outdir, name, step, **kwargs):
    if kwargs.get('conv_v2', False):
        kwargs.pop('conv_v2')
        tex_string = make_numerical_tex_string_conv_v2(step, **kwargs)
    else:
        tex_string = make_numerical_tex_string(step, **kwargs)
    # with open("./{}/{}.tex".format(outdir, name), "w") as f:
    #     f.write(tex_string.decode("utf-8"))
    jobname = '{}_{:02d}'.format(name, step)
    p = subprocess.Popen(['pdflatex', '-jobname={}'.format(jobname),
                          '-output-directory', outdir],
                         stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE)
    stdoutdata, stderrdata = p.communicate(input=tex_string)
    # Remove logs and aux if compilation was successfull
    if '! LaTeX Error' in stdoutdata.decode("utf-8") or '! Emergency stop' in stdoutdata.decode("utf-8"):
        print('! LaTeX Error: check the log file in {}/{}.log'.format(outdir, jobname))
    else:
        os.remove('./{}/{}.aux'.format(outdir, jobname))
        os.remove('./{}/{}.log'.format(outdir, jobname))


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser("Generate animate")
    parser.add_argument("mode", choices=["conv", "conv_transpose", "conv_v2"])

    args = parser.parse_args()
    
    Path(f"./201906_{args.mode}").mkdir(parents=True, exist_ok=True)

    if args.mode in ["conv", "conv_transpose"]:
        for i in range(25):
            compile_figure(f"201906_{args.mode}", "fig", step=i,
                        input_size=5,
                        output_size=3,
                        kernel_size=3,
                        transposed=True)
    else:
        for i in range(9):
            compile_figure(f"201906_{args.mode}", "fig", step=i,
                        input_size=5,
                        output_size=3,
                        kernel_size=3,
                        conv_v2=True)
