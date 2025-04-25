from ..core import *
import wx

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

        list_output = wx.ScrolledWindow(panel, style=wx.VSCROLL)
        list_output.SetScrollRate(0, 12)
        self.list_output = list_output
        list_output.sizer = wx.BoxSizer(wx.VERTICAL)
        list_output.SetSizer(list_output.sizer)
        panel.sizer.Add(list_output, wx.GBPosition(2, 0), wx.GBSpan(1, panel.cols), wx.EXPAND)

        status_output = wx.StaticText(panel)
        status_output.SetLabel("Try searching something")
        panel.sizer.Add(status_output, wx.GBPosition(1, 0), wx.GBSpan(1, panel.cols), wx.EXPAND)
        self.status_output = status_output

        # text_output = wx.TextCtrl(panel, 1, style=(wx.TE_MULTILINE | wx.TE_READONLY))
        # text_output.SetFont(wx.Font(12, wx.FONTFAMILY_TELETYPE, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))
        # self.text_output = text_output
        # panel.sizer.Add(text_output, wx.GBPosition(2, 0), wx.GBSpan(1, 3), wx.EXPAND)

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
        self.PrintResult(result)
        return

    def PrintResult(self, result):
        self.status_output.SetLabel(f"Found {len(result.result)} items")
        self.list_output.sizer.Clear(True)
        for item in result.result:
            item_text = f"{item.display} {item.name}\nunicode: {item.get_ucode()}, html: {item.get_htmlcode()}"
            item_view = wx.StaticText(self.list_output, 1, label=item_text)
            self.list_output.sizer.Add(item_view, 0, wx.BOTTOM, 10)
            item_view.Bind(wx.EVT_LEFT_UP, self.ShowDetails(item))
        self.list_output.Layout()
        self.list_output.FitInside()
        return

    def ShowDetails(self, item):
        def DoShowDetails(event):
            print(item.name) # this is a stub
        return DoShowDetails

class GuiWorker:
    def main(self):
        app = CharsWxApp()
        app.MainLoop()
        return 0
