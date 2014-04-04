# sssSDK 1.0 makefile

PREFIX=/usr

ECHO=@echo
MKDIR=mkdir -p
RM=rm -f
CP=cp -f

all:
	$(ECHO) "This package does not need to be built."

install:
	$(RM) -r $(PREFIX)/lib/blender/scripts/addons/sssSDK
	$(MKDIR) $(PREFIX)/lib/blender/scripts/addons/sssSDK
	$(CP) __init__.py $(PREFIX)/lib/blender/scripts/addons/sssSDK/
	$(CP) -r objects $(PREFIX)/lib/blender/scripts/addons/sssSDK/
	$(CP) -r scripts $(PREFIX)/lib/blender/scripts/addons/sssSDK/

clean:
	$(ECHO) "This package does not need to be cleaned."

