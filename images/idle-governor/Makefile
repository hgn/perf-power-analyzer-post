PYTHON_FILES := $(wildcard *.py)
IMAGE_FILES := $(PYTHON_FILES:.py=.png)
PDF_FILES := $(PYTHON_FILES:.py=.pdf)

all: $(IMAGE_FILES)

%.png: %.py
	python3 $<

clean:
	rm -f $(IMAGE_FILES) $(PDF_FILES)
