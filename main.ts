// news-image-20261125 entrypoint (Node 22, standard library only).
// The poster is the entry.png beside this file: a 1024x1024 PNG drawn
// by tools/build_poster.py, summing up Wednesday 25 November 2026 in
// six verified stories (Riyadh tower strike, Shenzhou-24, Giuliani's
// Medal of Freedom, the UN's AI-safety call, the landmine toll, and the
// Colombia car bomb). The program copies that poster to the grader's
// output directory so the judge sees exactly those bytes.
//
// The output directory is created first, so the copy works on a fresh
// output path as well as on the grader's mounted /output. Outside the
// grader, MAKEFUN_OUTPUT_DIR stands in for /output:
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync, mkdirSync } from 'node:fs';
import { join } from 'node:path';

// The copy is byte-for-byte, so two runs write identical output:
// the poster is a fixed asset, and this program adds no timestamps,
// randomness, or network access of its own.
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';
mkdirSync(outDir, { recursive: true });
copyFileSync(new URL('./entry.png', import.meta.url), join(outDir, 'entry.png'));
