import argparse
import re
import os

def escape(line):
    line = line.replace("_","\_")
    line = line.replace("^","\^")
    line = line.replace("\\{","\\\\{")
    line = line.replace("\\}","\\\\}")
    return line

def line_split(inp_line, out_lines):
    if inp_line.find("$$") > -1:
        seps = inp_line.split("$$")
        for i, sep in enumerate(seps):
            # $$ だけの行の場合は空と改行コードだけに分割されるため、その考慮
            if sep == "\n":
                continue
            # 文章の最終行が$$, この場合自動で改行コードが入るためこちらではいれず.
            if i + 1 ==  len(seps):
                out_lines.append(sep)
            else:
                out_lines.append(sep + "$$" + "\n")
    elif inp_line.find("$") > -1:
        # $$ で別れた最終行,元から改行コードが入るためこちらではいれず.
        seps = inp_line.split("$")
        for i,sep in enumerate(seps):
            if i+ 1 ==  len(seps):
                out_lines.append(sep)
            else:
                out_lines.append(sep + "$" + "\n")
    else:
        out_lines.append(inp_line)


def main(args):
    # OSの考慮
    enc = "utf-8" if os.name == "posix" else "utf-8_sig"
    
    lines = []
    g = open(args.output,"w", encoding=enc)
    
    
    
    """
    read file and split by math symbol $$ or $
    """
    with open(args.input, encoding=enc) as f:
        # $$,$を1行に最大一つまでにする.
        for line in f:
            line_split(line, lines)
    

        inline_flag = 0
        block_flag = 0
        table_flag = 0
        """
        - table内: 1行にする
        - inline $~$ => [tex: {~}], ~内は特殊文字をescape
        - block $$~$$ => [tex: {\displaystyle~}], ~内は特殊文字をescape
        - math ```math~``` => [tex: {\displaystyle~}], ~内は特殊文字をescape
        """
        for line in lines:
            # TODO これ以外でも検知できるようにする.
            table_st = line.find("|:-")
            # table の終わりの運用で検知して止める.
            table_end = line.find("|||")
            start_d = line.find("$")
            start_dd = line.find("$$")
            start_math =  line.find("```math")
            end_math =  line.find("```")
            # block flagは$$数式の中の意味
            if is_paragraph(line):
                line = "##" + line
            
            if start_dd > -1 and block_flag == 0:
                block_flag = 1
                w_line = line[:start_dd] + "[tex: { \displaystyle" + escape(line[start_dd+2:])
            elif start_dd > -1:
                block_flag = 0
                w_line = escape(line[:start_dd]) + "}]" + line[start_dd+2:]
            elif start_math > -1:
                block_flag = 1
                w_line = line[:start_math] + "[tex: { \displaystyle" + escape(line[start_math+7:])
            elif end_math > -1 and block_flag:
                block_flag = 0
                w_line = escape(line[:start_math]) + "}]" + line[start_math+3:]
            elif start_d > -1 and inline_flag == 0:
                inline_flag = 1
                w_line = line[:start_d] + "[tex: {" + escape(line[start_d+1:])
            elif start_d > -1:
                inline_flag = 0
                w_line = escape(line[:start_d]) + "}]" + line[start_d+1:]
            elif inline_flag or block_flag:
                w_line = escape(line)
                print("OK")
            else:
                w_line = line
            #if w_line.find("\{") > -1:
            #    import IPython;IPython.embed()
            if table_st > -1:
                table_flag = 1
                print("tablest",table_flag)
            if table_end > -1:
                table_flag = 0
                w_line = w_line.replace("|||","|")
            if  (table_flag and table_st == -1) or inline_flag :
                # table内は一行にまとめる. 
                #import IPython;IPython.embed()
                g.write(w_line[:-1])
            else:
                g.write(w_line)
    g.close()

def is_paragraph(line):
    # 1文字目 or スペースを無視した場合に
    return True if line.replace(" ","").find("#") == 0 else False
    


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='markdown 2 hatena')
    parser.add_argument('--input',"-i", type=str,default="input.md",
                        help='input file')
    parser.add_argument('--output',"-o", type=str,default="output.md",
                        help='ouput file')
    args = parser.parse_args()
    main(args)