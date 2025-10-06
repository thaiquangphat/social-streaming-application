find  app infra \
  -type f \
  -not -path "*/weight/*" \
  -not -path "*/chunkformer/*"\
  -not -path "Dockerfile"\
  -not -path "*/model/*"\
  -not -path "*/transnet_v2/*" \
  -not -path "*/beit3_components/*" \
  -not -path "*/LanguageBind/*" \
  -not -path "*/__pycache__/*" \
  -not -name "*.pyc" \
  -not -name "*.pyo" \
| while read f; do
    echo "===== $f ====="
    cat "$f"
    echo -e "\n"
done > output.txt
