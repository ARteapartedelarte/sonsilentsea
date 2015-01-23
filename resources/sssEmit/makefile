# sssEmit 1.0 makefile

ECHO=@echo
MKDIR=mkdir -p
RM=rm -f
CP=cp

ifndef $(ADDONS_PATH)
	ifndef $(PREFIX)
		PREFIX=/usr
	endif
	ADDONS_PATH=$(PREFIX)/lib/blender/scripts/addons
endif

all: install

clean: uninstall

install: uninstall
	$(MKDIR) $(ADDONS_PATH)/sssEmit
	$(CP) __init__.py $(ADDONS_PATH)/sssEmit/
	$(CP) -r particle $(ADDONS_PATH)/sssEmit/
	$(CP) -r scripts $(ADDONS_PATH)/sssEmit/

uninstall:
	$(RM) -r $(ADDONS_PATH)/sssEmit
