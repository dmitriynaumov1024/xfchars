from ..core import *
import wx
import wx.html

tags_no_content = [
    "br", "input", "img"
]

# oh no, i'm writing a hyperscript function again
def h (tag, children=None):
    tag = tag.strip()
    tagname = tag.split()[0]
    if tagname in tags_no_content:
        return f"<{tag}/>"
    if children is None:
        return f"<{tag}></{tagname}>"
    elif type(children) is list:
        return f"<{tag}>{str.join("", children)}</{tagname}>"
    else:
        return f"<{tag}>{children}</{tagname}>"


class CharsWxApp(wx.App):
    def OnInit(self):
        w = wx.Frame(None, -1, "Chars", 
            style=(wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX | wx.CLIP_CHILDREN | wx.RESIZE_BORDER))
        self.main_window = w

        panel = wx.Panel(w)
        
        panel.rows = 3
        panel.cols = 8

        panel.sizer = wx.GridBagSizer(4, 4)
        panel.sizer.SetRows(panel.rows)
        panel.sizer.SetCols(panel.cols)
        for col in range(panel.cols):
            panel.sizer.AddGrowableCol(col, proportion=1)
        panel.sizer.AddGrowableRow(panel.rows - 1)

        input_1 = wx.TextCtrl(panel, -1, style=wx.TE_LEFT)
        self.query_input = input_1
        panel.sizer.Add(input_1, wx.GBPosition(0, 0), wx.GBSpan(1, panel.cols - 3), (wx.EXPAND))

        button_settings = wx.Button(panel, -1, "\u26ed")
        button_settings.SetCanFocus(False)
        size = button_settings.GetMinSize()
        button_settings.SetMinSize((20, size[1]))
        panel.sizer.Add(button_settings, wx.GBPosition(0, panel.cols - 3), wx.GBSpan(1, 1), wx.EXPAND)

        button_search = wx.Button(panel, -1, "Search")
        button_search.SetCanFocus(False)
        button_search.Bind(wx.EVT_BUTTON, self.OnSearchButtonClick)
        panel.sizer.Add(button_search, wx.GBPosition(0, panel.cols - 2), wx.GBSpan(1, 2), wx.EXPAND)
        
        status_output = wx.StaticText(panel)
        status_output.SetLabel("Try searching something")
        panel.sizer.Add(status_output, wx.GBPosition(1, 0), wx.GBSpan(1, panel.cols), wx.EXPAND)
        self.status_output = status_output

        web_output = wx.html.HtmlWindow(panel)
        web_output.Bind(wx.html.EVT_HTML_LINK_CLICKED, self.OnWebItemClick)
        panel.sizer.Add(web_output, wx.GBPosition(2, 0), wx.GBSpan(1, panel.cols), wx.EXPAND)
        self.web_output = web_output

        panel.SetSizer(panel.sizer)

        w.sizer = wx.BoxSizer(wx.VERTICAL)
        w.sizer.Add(panel, 1, (wx.ALL | wx.EXPAND), border=4)

        w.SetSizer(w.sizer)

        w.SetMinSize(wx.Size(540, 660))

        w.Show()
        return True

    def OnSearchButtonClick(self, event):
        kwargs = dict(
            query = self.query_input.GetValue()
        )
        request = CharacterSearchRequest().set_values(**kwargs)
        result = CharacterSearcher.search(request)
        self.SetResult(result)
        return

    def OnWebItemClick(self, event):
        href = event.GetLinkInfo().GetHref()
        if href is None:
            return
        elif href == "copy-ucode":
            self.CopyToClipboard(self.active_item.get_ucode())
            return
        elif href == "copy-html":
            self.CopyToClipboard(self.active_item.get_htmlcode())
            return
        elif href == "back-to-result":
            self.BackToResult()
            return
        else:
            try:
                index = int(href)
                self.ShowDetails(self.result.result[index])
            except BaseException as e:
                print(e)
                pass
        return

    def SetResult(self, result):
        self.result = result
        html_ul_items = []
        for index, item in enumerate(result.result):
            html_ul_items.append(h("li", [
                h("p", [
                    h("font size=+1", [
                        str(item.display), " ",
                        h(f"a href={index}", item.name)
                    ]),
                    h("br"),
                    h("span", f"unicode: {item.get_ucode()}, html: {item.get_htmlcode_esc()}"),
                    h("br")
                ])
            ]))
        self.html_doc = h("html", [
            h("body", [
                h("ol", html_ul_items)
            ])
        ])
        self.status_text = f"Found {len(self.result.result)} items. Click on item name to see details."
        self.status_output.SetLabel(self.status_text)
        self.web_output.SetPage(self.html_doc)
        return

    def BackToResult(self):
        self.status_output.SetLabel(self.status_text)
        self.web_output.SetPage(self.html_doc)
        self.web_output.Scroll(0, self.web_output.old_scroll)
        return

    def ShowDetails(self, item):
        self.active_item = item
        details_html_doc = h("html", [
            h("body", [
                h("p", [
                    h("font size=+4", item.display), " ",
                    h("font size=+1", item.name),
                ]),
                h("p", [
                    h("span", f"unicode: {item.get_ucode()}"), " ",
                    h("a href=copy-ucode", "copy")
                ]),
                h("p", [
                    h("span", f"html: {item.get_htmlcode_esc()}"), " ",
                    h("a href=copy-html", "copy")
                ]),
                h("br"),
                h("br"),
                h("p", [
                    h("a href=back-to-result", "Back to search result")
                ])
            ])
        ])
        self.web_output.old_scroll = self.web_output.GetScrollPos(wx.VERTICAL)
        self.status_output.SetLabel(f"Found {len(self.result.result)} items. Viewing {item.get_ucode()}.")
        self.web_output.SetPage(details_html_doc)
        return

    def CopyToClipboard(self, text):
        cb = wx.TheClipboard
        print("Should copy this:", text)
        if cb.Open():
            cb.SetData(wx.TextDataObject(text))
            cb.Close()


class GuiWorker:
    def main(self):
        app = CharsWxApp()
        app.MainLoop()
        return 0
