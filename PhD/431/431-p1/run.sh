echo 'A new run' >> output.txt
echo 'Running code0_0' >> output.txt
python3 main.py --num-regs 32 --dm-size 65 --cpu-type singlecycle --mips-code code0_0.txt >> output.txt
echo 'Running code0_1' >> output.txt
python3 main.py --num-regs 32 --dm-size 65 --cpu-type singlecycle --mips-code code0_1.txt >> output.txt
echo 'Running code0_2' >> output.txt
python3 main.py --num-regs 32 --dm-size 65 --cpu-type vliw --mips-code code0_2.txt --issue-width 2 >> output.txt
echo 'Running code0_3' >> output.txt
python3 main.py --num-regs 32 --dm-size 65 --cpu-type vliw --mips-code code0_3.txt --issue-width 2 >> output.txt
echo 'Running code1_0' >> output.txt
python3 main.py --num-regs 32 --dm-size 65 --cpu-type singlecycle --mips-code code1_0.txt >> output.txt
echo 'Running code1_1' >> output.txt
python3 main.py --num-regs 32 --dm-size 65 --cpu-type singlecycle --mips-code code1_1.txt >> output.txt
echo 'Running code1_2' >> output.txt
python3 main.py --num-regs 32 --dm-size 65 --cpu-type vliw --mips-code code1_2.txt --issue-width 2 >> output.txt
echo 'Running code1_3' >> output.txt
python3 main.py --num-regs 32 --dm-size 65 --cpu-type vliw --mips-code code1_3.txt --issue-width 2 >> output.txt
echo 'Running code1_4' >> output.txt
python3 main.py --num-regs 32 --dm-size 65 --cpu-type vliw --mips-code code1_4.txt --issue-width 4 >> output.txt
echo 'Running code1_5' >> output.txt
python3 main.py --num-regs 32 --dm-size 65 --cpu-type vliw --mips-code code1_5.txt --issue-width 4 >> output.txt