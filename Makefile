.PHONY: brand-guide ebook verify-ebook

BRAND_GUIDE_PDF := brand/Specsfy-Manual-de-Marca.pdf
BRAND_GUIDE_SOURCES := \
	brand/guide/brand-guide.md \
	brand/guide/template.html \
	brand/style-guide.html \
	brand/logo/LOGO.md \
	brand/logo/icon.svg \
	brand/logo/icon.png \
	.pdf/build-brand-guide.sh \
	.pdf/style.css

brand-guide: $(BRAND_GUIDE_PDF)

$(BRAND_GUIDE_PDF): $(BRAND_GUIDE_SOURCES)
	./.pdf/build-brand-guide.sh

EBOOK_DOC_SOURCES := $(shell find docs/user -type f -print)
EBOOK_BUILD_SOURCES := \
	ebook/VERSION \
	docs/user/reading-order.txt \
	.ebook/build-ebook.sh \
	.ebook/extract-document-metadata.py \
	.ebook/external-links.lua \
	.ebook/strip-document-metadata.lua \
	.ebook/metadata.yaml \
	.ebook/template.html \
	.ebook/pdf.css \
	.ebook/epub.css \
	brand/logo/icon.svg \
	brand/logo/icon.png \
	brand/style-guide.html

ebook: $(EBOOK_DOC_SOURCES) $(EBOOK_BUILD_SOURCES)
	./.ebook/build-ebook.sh

verify-ebook:
	./.ebook/build-ebook.sh --check
