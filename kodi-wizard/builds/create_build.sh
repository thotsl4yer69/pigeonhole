#!/bin/bash
#
# Pigeon Build Creator
# Creates professional Kodi builds for distribution
#

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
KODI_HOME="$HOME/.kodi"
BUILD_DIR="$SCRIPT_DIR/output"
TEMP_DIR="$SCRIPT_DIR/temp"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Banner
echo -e "${BLUE}"
cat << "EOF"
╔══════════════════════════════════════════════╗
║  🐦 PIGEON BUILD CREATOR                    ║
║  Professional Kodi Build Packager           ║
╚══════════════════════════════════════════════╝
EOF
echo -e "${NC}"

# Functions
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[✓]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[!]${NC} $1"
}

log_error() {
    echo -e "${RED}[✗]${NC} $1"
}

check_kodi() {
    if [ ! -d "$KODI_HOME" ]; then
        log_error "Kodi home directory not found: $KODI_HOME"
        log_info "Please run Kodi at least once to create the directory"
        exit 1
    fi
    log_success "Found Kodi installation at $KODI_HOME"
}

check_requirements() {
    log_info "Checking requirements..."

    local missing=0

    if ! command -v zip &> /dev/null; then
        log_error "zip command not found. Install: sudo apt install zip"
        missing=1
    fi

    if ! command -v md5sum &> /dev/null; then
        log_error "md5sum command not found"
        missing=1
    fi

    if [ $missing -eq 1 ]; then
        exit 1
    fi

    log_success "All requirements met"
}

show_menu() {
    echo ""
    echo -e "${BLUE}Select build type to create:${NC}"
    echo ""
    echo "  1) Pigeon Essential (Fire TV Stick 1GB)"
    echo "  2) Pigeon Pro (Fire TV Stick 4K 2GB)"
    echo "  3) Pigeon Ultimate (Shield/PC 4GB+)"
    echo "  4) Create all builds"
    echo "  5) Exit"
    echo ""
    read -p "Enter choice [1-5]: " choice

    case $choice in
        1) create_build "essential" "Pigeon Essential" "Fire TV Stick 1GB";;
        2) create_build "pro" "Pigeon Pro" "Fire TV Stick 4K";;
        3) create_build "ultimate" "Pigeon Ultimate" "Shield/PC";;
        4) create_all_builds;;
        5) exit 0;;
        *) log_error "Invalid choice"; show_menu;;
    esac
}

create_build() {
    local build_id="$1"
    local build_name="$2"
    local build_target="$3"

    echo ""
    echo -e "${BLUE}════════════════════════════════════════════${NC}"
    echo -e "${BLUE}Creating: $build_name${NC}"
    echo -e "${BLUE}Target: $build_target${NC}"
    echo -e "${BLUE}════════════════════════════════════════════${NC}"
    echo ""

    # Create directories
    mkdir -p "$BUILD_DIR"
    mkdir -p "$TEMP_DIR"

    local build_temp="$TEMP_DIR/build_${build_id}"
    rm -rf "$build_temp"
    mkdir -p "$build_temp"

    # Step 1: Copy Kodi data
    log_info "Step 1/7: Copying Kodi configuration..."

    # Copy essential directories
    if [ -d "$KODI_HOME/addons" ]; then
        cp -r "$KODI_HOME/addons" "$build_temp/"
        log_success "Copied addons"
    fi

    if [ -d "$KODI_HOME/userdata" ]; then
        cp -r "$KODI_HOME/userdata" "$build_temp/"
        log_success "Copied userdata"
    fi

    # Step 2: Clean sensitive/cache data
    log_info "Step 2/7: Cleaning sensitive data..."

    # Remove cache and thumbnails
    rm -rf "$build_temp/userdata/Thumbnails"
    rm -rf "$build_temp/userdata/Database/Textures"*.db*
    find "$build_temp" -type d -name "cache" -exec rm -rf {} + 2>/dev/null || true
    find "$build_temp" -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
    find "$build_temp" -name "*.pyc" -delete 2>/dev/null || true

    log_success "Cleaned cache and temporary files"

    # Step 3: Apply build-specific settings
    log_info "Step 3/7: Applying build-specific configuration..."

    # Copy appropriate advancedsettings.xml
    case $build_id in
        essential)
            cp "$SCRIPT_DIR/../advanced_settings/firestick_1gb.xml" \
               "$build_temp/userdata/advancedsettings.xml" 2>/dev/null || true
            ;;
        pro)
            cp "$SCRIPT_DIR/../advanced_settings/firestick_2gb.xml" \
               "$build_temp/userdata/advancedsettings.xml" 2>/dev/null || true
            ;;
        ultimate)
            cp "$SCRIPT_DIR/../advanced_settings/pc_4gb_plus.xml" \
               "$build_temp/userdata/advancedsettings.xml" 2>/dev/null || true
            ;;
    esac

    log_success "Applied advanced settings for $build_target"

    # Step 4: Add setup guide
    log_info "Step 4/7: Adding setup guide..."

    cp "$SCRIPT_DIR/SETUP_GUIDE.txt" "$build_temp/"

    # Create build info file
    cat > "$build_temp/BUILD_INFO.txt" << EOF
Pigeon Build - $build_name
Version: 1.0
Target Device: $build_target
Created: $(date)
Build ID: $build_id

This is a complete Kodi installation optimized for streaming.

Quick Start:
1. Extract this ZIP to your Kodi userdata folder
2. Follow SETUP_GUIDE.txt for Trakt and Real-Debrid
3. Start streaming!

Support: https://github.com/thotsl4yer69/pigeonhole
EOF

    log_success "Added documentation"

    # Step 5: Create package
    log_info "Step 5/7: Creating ZIP package..."

    local zip_name="pigeon-${build_id}-$(date +%Y%m%d).zip"
    local zip_path="$BUILD_DIR/$zip_name"

    cd "$build_temp"
    zip -r "$zip_path" . -q
    cd "$SCRIPT_DIR"

    log_success "Created package: $zip_name"

    # Step 6: Calculate checksums
    log_info "Step 6/7: Calculating checksums..."

    local md5=$(md5sum "$zip_path" | awk '{print $1}')
    local size=$(du -h "$zip_path" | awk '{print $1}')

    log_success "Size: $size"
    log_success "MD5: $md5"

    # Create checksum file
    echo "$md5  $zip_name" > "$zip_path.md5"

    # Step 7: Create build metadata
    log_info "Step 7/7: Creating metadata..."

    cat > "$BUILD_DIR/${build_id}_metadata.json" << EOF
{
  "name": "$build_name",
  "version": "1.0",
  "build_id": "$build_id",
  "target": "$build_target",
  "filename": "$zip_name",
  "size": "$size",
  "md5": "$md5",
  "created": "$(date -Iseconds)",
  "url": "https://github.com/thotsl4yer69/pigeonhole/releases/download/v1.0/$zip_name",
  "download_url": "https://github.com/thotsl4yer69/pigeonhole/releases/download/v1.0/$zip_name",
  "info": "Optimized for $build_target"
}
EOF

    log_success "Created metadata"

    # Cleanup temp
    rm -rf "$build_temp"

    echo ""
    echo -e "${GREEN}════════════════════════════════════════════${NC}"
    echo -e "${GREEN}✓ BUILD COMPLETE!${NC}"
    echo -e "${GREEN}════════════════════════════════════════════${NC}"
    echo ""
    echo -e "  Build: ${BLUE}$build_name${NC}"
    echo -e "  File: ${BLUE}$zip_name${NC}"
    echo -e "  Size: ${BLUE}$size${NC}"
    echo -e "  MD5: ${BLUE}$md5${NC}"
    echo -e "  Location: ${BLUE}$zip_path${NC}"
    echo ""
}

create_all_builds() {
    log_info "Creating all builds..."
    echo ""

    create_build "essential" "Pigeon Essential" "Fire TV Stick 1GB"
    echo ""
    create_build "pro" "Pigeon Pro" "Fire TV Stick 4K"
    echo ""
    create_build "ultimate" "Pigeon Ultimate" "Shield/PC"

    echo ""
    echo -e "${GREEN}════════════════════════════════════════════${NC}"
    echo -e "${GREEN}✓ ALL BUILDS COMPLETE!${NC}"
    echo -e "${GREEN}════════════════════════════════════════════${NC}"
    echo ""
    echo "Builds created in: $BUILD_DIR"
    echo ""
    ls -lh "$BUILD_DIR"/*.zip
    echo ""
}

# Main execution
check_kodi
check_requirements

# Check if current Kodi has addons installed
if [ ! -d "$KODI_HOME/addons/plugin.video.thecrew" ]; then
    log_warning "The Crew addon not found in current Kodi installation"
    log_info "Please install addons via Pigeon Wizard first:"
    echo ""
    echo "  1. Launch Kodi"
    echo "  2. Open Pigeon Build Wizard"
    echo "  3. Install Add-ons → The Crew, The Loop, Umbrella"
    echo "  4. Configure addons (optional)"
    echo "  5. Run this script again"
    echo ""
    read -p "Continue anyway? [y/N]: " continue
    if [[ ! $continue =~ ^[Yy]$ ]]; then
        exit 0
    fi
fi

show_menu
