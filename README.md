# NIST SP 800-53r5 RAG Chatbot

A local RAG chatbot for NIST SP 800-53 Revision 5 controls.

## Usage

1. Add your NIST PDF(s) to [docs](http://_vscodecontentref_/15).
2. Run [ingest.py](http://_vscodecontentref_/16) to build the index.
3. Deploy on Streamlit Cloud.
4. Set your [GOOGLE_API_KEY](http://_vscodecontentref_/17) in Streamlit secrets.

## Local Development

```sh
pip install -r requirements.txt
python ingest.py
streamlit run app.py
