import unittest
from main import extract_title, generate_page

class TestMain(unittest.TestCase):

    def test_extract_title(self):
        markdown = """
# This is the title with no white space
## Subtitle
 '''
 Bunch of code
 '''

 **Some bold text**
 The end
        """
        test = extract_title(markdown)
        self.assertEqual(test, "This is the title with no white space")


    def test_extract_title_ws(self):
        markdown = """
# This is the title with some white space       
## Subtitle
 '''
 Bunch of code
 '''

 **Some bold text**
 The end
        """
        test = extract_title(markdown)
        self.assertEqual(test, "This is the title with some white space")

    def test_extract_title_dws(self):
        markdown = """
#      This is the title with a lot of white space            
## Subtitle
 '''
 Bunch of code
 '''

 **Some bold text**
 The end
        """
        test = extract_title(markdown)
        self.assertEqual(test, "This is the title with a lot of white space")


    def test_extract_multiple_titles(self):
        markdown = """
# This is the title with no white space
## Subtitle
 '''
 Bunch of code
 '''
# Another title
 **Some bold text**
 The end
        """
        test = extract_title(markdown)
        self.assertEqual(test, "This is the title with no white space")        
        self.assertNotEqual(test, "Another title")


    def test_generate_page_existing_target(self):
        self.maxDiff = None
        generate_page("content/index.md", "template.html", "content/test_existing_output.html")
        with open("content/test_existing_output.html", "r") as f:
            test = f.read()
        expected = """<!doctype html>
<html>
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>Tolkien Fan Club</title>
    <link href="/index.css" rel="stylesheet" />
  </head>

  <body>
    <article><div><h1>Tolkien Fan Club</h1><p><img src="/images/tolkien.png" alt="JRR Tolkien sitting"></img></p><p>Here's the deal, <b>I like Tolkien</b>.</p><blockquote>"I am in fact a Hobbit in all but size."  -- J.R.R. Tolkien</blockquote><h2>Blog posts</h2><ul><li><a href="/blog/glorfindel">Why Glorfindel is More Impressive than Legolas</a></li><li><a href="/blog/tom">Why Tom Bombadil Was a Mistake</a></li><li><a href="/blog/majesty">The Unparalleled Majesty of "The Lord of the Rings"</a></li></ul><h2>Reasons I like Tolkien</h2><ul><li>You can spend years studying the legendarium and still not understand its depths</li><li>It can be enjoyed by children and adults alike</li><li>Disney <i>didn't ruin it</i> (okay, but Amazon might have)</li><li>It created an entirely new genre of fantasy</li></ul><h2>My favorite characters (in order)</h2><ol><li>Gandalf</li><li>Bilbo</li><li>Sam</li><li>Glorfindel</li><li>Galadriel</li><li>Elrond</li><li>Thorin</li><li>Sauron</li><li>Aragorn</li></ol><p>Here's what <code>elflang</code> looks like (the perfect coding language):</p><pre><code>func main(){
fmt.Println("Aiya, Ambar!")
}
</code></pre><p>Want to get in touch? <a href="/contact">Contact me here</a>.</p><p>This site was generated with a custom-built <a href="https://www.boot.dev/courses/build-static-site-generator-python">static site generator</a> from the course on <a href="https://www.boot.dev">Boot.dev</a>.</p></div></article>
  </body>
</html>
"""
        self.assertEqual(expected, test)


if __name__ == "__main__":
    unittest.main()
