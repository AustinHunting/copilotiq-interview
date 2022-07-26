FROM alpine:3.16.1
RUN apk add python3 py3-pip
RUN pip3 install requests==2.22.0 beautifulSoup4==4.11.1
WORKDIR /home
COPY hyperlinks.py /hyperlinks.py
ENTRYPOINT [ "/hyperlinks.py" ]

# build with:
#   docker build -t hyperlinks .

# run with:
#   docker run --rm -it -v /tmp/hmmmm:/home/ hyperlinks --url=https://example.com --limit=4 --out=out.json