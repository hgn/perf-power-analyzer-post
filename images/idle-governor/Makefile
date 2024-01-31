PYTHON_FILES := $(wildcard *.py)
IMAGE_FILES := $(PYTHON_FILES:.py=.png)
PDF_FILES := $(PYTHON_FILES:.py=.pdf)
SCATTER_FOLDER := cstates

all: $(IMAGE_FILES)

%.png: %.py
	python3 $<

clean:
	rm -f $(IMAGE_FILES) $(PDF_FILES)
	rm -rf $(SCATTER_FOLDER)
