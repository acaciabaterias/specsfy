.PHONY: brand-guide

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
