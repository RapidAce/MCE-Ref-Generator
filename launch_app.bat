@echo off
cd /d %~dp0
echo Starting the MCE Reference Generator...
streamlit run mce_ref_generator.py --server.address=0.0.0.0 --server.port=8501
pause
