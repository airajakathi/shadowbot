class Praisonai < Formula
    include Language::Python::Virtualenv
  
    desc "AI tools for various AI applications"
    homepage "https://github.com/MervinPraison/ShadowBot"
    url "https://github.com/MervinPraison/ShadowBot/archive/refs/tags/v4.6.37.tar.gz"
    sha256 `curl -sL https://github.com/MervinPraison/ShadowBot/archive/refs/tags/v4.6.37.tar.gz | shasum -a 256`.split.first
    license "MIT"
  
    depends_on "python@3.11"
  
    def install
      virtualenv_install_with_resources
    end
  
    test do
      system "#{bin}/shadowbot", "--version"
    end
  end
  