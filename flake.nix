{
  description = "Historical K(t) Index - Measuring Global Civilizational Coherence";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = { self, nixpkgs, flake-utils }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = nixpkgs.legacyPackages.${system};

        # Python with Poetry for dependency management
        pythonEnv = pkgs.python311;

      in
      {
        devShells.default = pkgs.mkShell {
          buildInputs = with pkgs; [
            # Python and Poetry
            pythonEnv
            poetry

            # System dependencies for Python packages
            gcc
            pkg-config

            # Geospatial libraries (for geopandas)
            gdal
            geos
            proj

            # Scientific computing
            hdf5
            netcdf

            # Development tools
            git

            # Optional: Data download tools
            curl
            wget

            # LaTeX for PDF generation (full scheme for all packages)
            texlive.combined.scheme-full
            pandoc
            librsvg  # For SVG to PDF conversion
          ];

          shellHook = ''
            echo "🌍 Historical K(t) Index Development Environment"
            echo "=================================================="
            echo ""
            echo "Python: $(python --version)"
            echo "Poetry: $(poetry --version)"
            echo ""
            echo "📊 Setup:"
            echo "  1. Initialize Poetry (if first time): poetry install"
            echo "  2. Activate environment: poetry shell"
            echo "  3. Run scripts: poetry run python scripts/..."
            echo ""
            echo "🔬 Data Collection Scripts Ready:"
            echo "  - 01_download_wipo_patents.py"
            echo "  - 02_download_ccp_constitutions.py"
            echo "  - 03_download_barro_lee_education.py"
            echo "  - 04_construct_infrastructure_index.py"
            echo "  - 05_integrate_H7_components.py"
            echo ""
            echo "📚 Quick Start: cat QUICK_START.md"
            echo ""
            echo "Ready to build validated H₇ component! 🚀"
            echo ""
          '';

          # Set environment variables
          POETRY_VIRTUALENVS_IN_PROJECT = "true";
          LD_LIBRARY_PATH = pkgs.lib.makeLibraryPath [
            pkgs.stdenv.cc.cc
            pkgs.gdal
            pkgs.geos
            pkgs.proj
          ];
        };

        # CI environment (minimal, fast)
        devShells.ci = pkgs.mkShell {
          buildInputs = with pkgs; [
            pythonEnv
            poetry
          ];
        };
      }
    );
}
