#!/bin/bash

set -o errexit

if [ ! "$1" ]; then
  echo "This script requires either amd64 of arm64 as an argument"
	exit 1
elif [ "$1" = "amd64" ]; then
	PLATFORM="amd64"
else
	PLATFORM="arm64"
fi
export PLATFORM

git status
git submodule

# If the env variable NOTARIZE and the username and password variables are
# set, this will attempt to Notarize the signed DMG

if [ ! "$DOGECHIA_INSTALLER_VERSION" ]; then
	echo "WARNING: No environment variable DOGECHIA_INSTALLER_VERSION set. Using 0.0.0."
	DOGECHIA_INSTALLER_VERSION="0.0.0"
fi
echo "Dogechia Installer Version is: $DOGECHIA_INSTALLER_VERSION"
export DOGECHIA_INSTALLER_VERSION

echo "Installing npm and electron packagers"
cd npm_linux || exit 1
npm ci
PATH=$(npm bin):$PATH
cd .. || exit 1

echo "Create dist/"
rm -rf dist
mkdir dist

echo "Create executables with pyinstaller"
SPEC_FILE=$(python -c 'import dogechia; print(dogechia.PYINSTALLER_SPEC_PATH)')
pyinstaller --log-level=INFO "$SPEC_FILE"
LAST_EXIT_CODE=$?
if [ "$LAST_EXIT_CODE" -ne 0 ]; then
	echo >&2 "pyinstaller failed!"
	exit $LAST_EXIT_CODE
fi

# Builds CLI only .deb
# need j2 for templating the control file
pip install j2cli
CLI_DEB_BASE="doge-chia-cli_$DOGECHIA_INSTALLER_VERSION-1_$PLATFORM"
mkdir -p "dist/$CLI_DEB_BASE/opt/dogechia"
mkdir -p "dist/$CLI_DEB_BASE/usr/bin"
mkdir -p "dist/$CLI_DEB_BASE/DEBIAN"
j2 -o "dist/$CLI_DEB_BASE/DEBIAN/control" assets/deb/control.j2
cp -r dist/daemon/* "dist/$CLI_DEB_BASE/opt/dogechia/"
ln -s ../../opt/dogechia/dogechia "dist/$CLI_DEB_BASE/usr/bin/dogechia"
dpkg-deb --build --root-owner-group "dist/$CLI_DEB_BASE"
# CLI only .deb done

cp -r dist/daemon ../dogechia-blockchain-gui/packages/gui

# Change to the gui package
cd ../dogechia-blockchain-gui/packages/gui || exit 1

# sets the version for doge-chia in package.json
cp package.json package.json.orig
jq --arg VER "$DOGECHIA_INSTALLER_VERSION" '.version=$VER' package.json > temp.json && mv temp.json package.json

echo "Building Linux(deb) Electron app"
PRODUCT_NAME="dogechia"
if [ "$PLATFORM" = "arm64" ]; then
  # electron-builder does not work for arm64 as of Aug 16, 2022.
  # This is a temporary fix.
  # https://github.com/jordansissel/fpm/issues/1801#issuecomment-919877499
  # @TODO Consolidates the process to amd64 if the issue of electron-builder is resolved
  sudo apt -y install ruby ruby-dev
  # `sudo gem install public_suffix -v 4.0.7` is required to fix the error below.
  #   ERROR:  Error installing fpm:
  #   The last version of public_suffix (< 6.0, >= 2.0.2) to support your Ruby & RubyGems was 4.0.7. Try installing it with `gem install public_suffix -v 4.0.7` and then running the current command again
  #   public_suffix requires Ruby version >= 2.6. The current ruby version is 2.5.0.
  # @TODO Maybe versions of sub dependencies should be managed by gem lock file.
  # @TODO Once ruby 2.6 can be installed on `apt install ruby`, installing public_suffix below should be removed.
  sudo gem install public_suffix -v 4.0.7
  sudo gem install fpm
  echo USE_SYSTEM_FPM=true electron-builder build --linux deb --arm64 \
    --config.extraMetadata.name=doge-chia \
    --config.productName="$PRODUCT_NAME" --config.linux.desktop.Name="Dogechia Blockchain" \
    --config.deb.packageName="doge-chia"
  USE_SYSTEM_FPM=true electron-builder build --linux deb --arm64 \
    --config.extraMetadata.name=doge-chia \
    --config.productName="$PRODUCT_NAME" --config.linux.desktop.Name="Dogechia Blockchain" \
    --config.deb.packageName="doge-chia"
  LAST_EXIT_CODE=$?
else
  echo electron-builder build --linux deb --x64 \
    --config.extraMetadata.name=doge-chia \
    --config.productName="$PRODUCT_NAME" --config.linux.desktop.Name="Dogechia Blockchain" \
    --config.deb.packageName="doge-chia"
  electron-builder build --linux deb --x64 \
    --config.extraMetadata.name=doge-chia \
    --config.productName="$PRODUCT_NAME" --config.linux.desktop.Name="Dogechia Blockchain" \
    --config.deb.packageName="doge-chia"
  LAST_EXIT_CODE=$?
fi
ls -l dist/linux*-unpacked/resources

# reset the package.json to the original
mv package.json.orig package.json

if [ "$LAST_EXIT_CODE" -ne 0 ]; then
	echo >&2 "electron-builder failed!"
	exit $LAST_EXIT_CODE
fi

GUI_DEB_NAME=doge-chia_${DOGECHIA_INSTALLER_VERSION}_${PLATFORM}.deb
mv "dist/${PRODUCT_NAME}-${DOGECHIA_INSTALLER_VERSION}.deb" "../../../build_scripts/dist/${GUI_DEB_NAME}"
cd ../../../build_scripts || exit 1

echo "Create final installer"
rm -rf final_installer
mkdir final_installer

mv "dist/${GUI_DEB_NAME}" final_installer/
# Move the cli only deb into final installers as well, so it gets uploaded as an artifact
mv "dist/${CLI_DEB_BASE}.deb" final_installer/

ls -l final_installer/
