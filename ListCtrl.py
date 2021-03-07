#!/usr/bin/env python

#----------------------------------------------------------------------------
# Name:         ListCtrl.py
# Purpose:      Testing lots of stuff, controls, window types, etc.
#
# Author:       Robin Dunn & Gary Dumer
#
# Created:
# Copyright:    (c) 1998-2020 by Total Control Software
# Licence:      wxWindows license
#----------------------------------------------------------------------------

import sys
import wx
import wx.lib.mixins.listctrl as listmix

import images


#---------------------------------------------------------------------------


#musicdata = OrderedDict() ##
musicdata = {
1 : ("1r", "The Price Of Love", "Rock"),
2 : ("2r", "Tom's Diner", "Rock"),
3 : ("3r", "Praying For Time", "Rock"),
4 : ("4r", "Here We Are", "Rock"),
5 : ("5r", "Don't Know Much", "Rock"),
6 : ("6r", "How Am I Supposed To Live Without You", "Blues"),
7 : ("7r", "Oh Girl", "Rock"),
8 : ("8r", "Opposites Attract", "Rock"),
9 : ("9r", "Should've Known Better", "Rock"),
10: ("10r", "Forever Young", "Rock"),
11: ("11r", "Dangerous", "Rock"),
12: ("12r", "The Lover In Me", "Rock"),
}


# lista = [
#     ['Club,', 'Country,', 'Rating']
#     ['Man', 'Utd,', 'England,', '7.05']
#     ['Man', 'City,', 'England,', '8.75']
#     ['Barcelona,', 'Spain,', '8.72']
#     ['Bayern', 'Munich,', 'Germany,', '8.75']
#     ['Liverpool,', 'England,', '8.81']
# ]


import csv ##

def get_dane_from_csv(file_name): ## mozna pozniej zrobic mozliwosc wyboru plikow inicjujacych
    lista = []
    slownik = {}

    with open('moj.csv', 'r') as f:
        reader = csv.reader(f, delimiter=',')
        for row in reader:
            lista.append(row)

    for wiersz in lista:
        slownik[wiersz[0]]=wiersz[1:]
    return slownik 

dane = get_dane_from_csv('moj.csv') ##
print(dane)

#---------------------------------------------------------------------------

class TestListCtrl(wx.ListCtrl, listmix.ListCtrlAutoWidthMixin):
    def __init__(self, parent, ID, pos=wx.DefaultPosition,
                 size=wx.DefaultSize, style=0):
        wx.ListCtrl.__init__(self, parent, ID, pos, size, style)
        listmix.ListCtrlAutoWidthMixin.__init__(self)


class TestListCtrlPanel(wx.Panel, listmix.ColumnSorterMixin):
    def __init__(self, parent, log):
        wx.Panel.__init__(self, parent, -1, style=wx.WANTS_CHARS)

        self.log = log
        tID = wx.NewIdRef()

        sizer = wx.BoxSizer(wx.VERTICAL)

        if wx.Platform == "__WXMAC__" and \
               hasattr(wx.GetApp().GetTopWindow(), "LoadDemo"):
            self.useNative = wx.CheckBox(self, -1, "Use native listctrl")
            self.useNative.SetValue(
                not wx.SystemOptions.GetOptionInt("mac.listctrl.always_use_generic") )
            self.Bind(wx.EVT_CHECKBOX, self.OnUseNative, self.useNative)
            sizer.Add(self.useNative, 0, wx.ALL | wx.ALIGN_RIGHT, 4)

        self.il = wx.ImageList(16, 16)

        self.idx1 = self.il.Add(images.Smiles.GetBitmap())
        self.sm_up = self.il.Add(images.SmallUpArrow.GetBitmap())
        self.sm_dn = self.il.Add(images.SmallDnArrow.GetBitmap())

        self.list = TestListCtrl(self, tID,
                                 style=wx.LC_REPORT
                                 #| wx.BORDER_SUNKEN
                                 | wx.BORDER_NONE
                                 | wx.LC_EDIT_LABELS
                                 #| wx.LC_SORT_ASCENDING    # disabling initial auto sort gives a
                                 #| wx.LC_NO_HEADER         # better illustration of col-click sorting
                                 #| wx.LC_VRULES
                                 #| wx.LC_HRULES
                                 #| wx.LC_SINGLE_SEL
                                 )

        self.list.SetImageList(self.il, wx.IMAGE_LIST_SMALL)
        sizer.Add(self.list, 1, wx.EXPAND)
        self.list.EnableCheckBoxes(enable=True)

        self.PopulateList()

        # Now that the list exists we can init the other base class,
        # see wx/lib/mixins/listctrl.py
        self.itemDataMap = dane ##
        listmix.ColumnSorterMixin.__init__(self, 3)
        

        #self.SortListItems(0, True)

        self.SetSizer(sizer)
        self.SetAutoLayout(True)

        self.Bind(wx.EVT_LIST_ITEM_SELECTED, self.OnItemSelected, self.list)
        self.Bind(wx.EVT_LIST_ITEM_DESELECTED, self.OnItemDeselected, self.list)
        self.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.OnItemActivated, self.list)
        self.Bind(wx.EVT_LIST_DELETE_ITEM, self.OnItemDelete, self.list)
        self.Bind(wx.EVT_LIST_COL_CLICK, self.OnColClick, self.list)
        self.Bind(wx.EVT_LIST_COL_RIGHT_CLICK, self.OnColRightClick, self.list)
        self.Bind(wx.EVT_LIST_COL_BEGIN_DRAG, self.OnColBeginDrag, self.list)
        self.Bind(wx.EVT_LIST_COL_DRAGGING, self.OnColDragging, self.list)
        self.Bind(wx.EVT_LIST_COL_END_DRAG, self.OnColEndDrag, self.list)
        self.Bind(wx.EVT_LIST_BEGIN_LABEL_EDIT, self.OnBeginEdit, self.list)
        self.Bind(wx.EVT_LIST_END_LABEL_EDIT, self.OnEndEdit, self.list)

        self.list.Bind(wx.EVT_LEFT_DCLICK, self.OnDoubleClick)
        self.list.Bind(wx.EVT_RIGHT_DOWN, self.OnRightDown)

        # for wxMSW
        self.list.Bind(wx.EVT_COMMAND_RIGHT_CLICK, self.OnRightClick)

        # for wxGTK
        self.list.Bind(wx.EVT_RIGHT_UP, self.OnRightClick)

    def OnUseNative(self, event):
        wx.SystemOptions.SetOption("mac.listctrl.always_use_generic", not event.IsChecked())
        wx.GetApp().GetTopWindow().LoadDemo("ListCtrl")

    def PopulateList(self):
        if 0:
            # for normal, simple columns, you can add them like this:
            self.list.InsertColumn(0, "Artist")
            self.list.InsertColumn(1, "Title", wx.LIST_FORMAT_RIGHT)
            self.list.InsertColumn(2, "Genre")
        else:
            # but since we want images on the column header we have to do it the hard way:
            info = wx.ListItem()
            info.Mask = wx.LIST_MASK_TEXT | wx.LIST_MASK_IMAGE | wx.LIST_MASK_FORMAT
            info.Image = -1
            info.Align = 0
            info.Text = "Artist"
            self.list.InsertColumn(0, info)

            info.Align = wx.LIST_FORMAT_RIGHT
            info.Text = "Title"
            self.list.InsertColumn(1, info)

            info.Align = 0
            info.Text = "Genre"
            self.list.InsertColumn(2, info)

        items = dane.items() ##
        for key, data in items:
            index = self.list.InsertItem(self.list.GetItemCount(), data[0], self.idx1)
            self.list.SetItem(index, 1, data[1])
            self.list.SetItem(index, 2, data[2])
            self.list.SetItemData(index, int(key)) ##
            print(key)

        self.list.SetColumnWidth(0, wx.LIST_AUTOSIZE)
        self.list.SetColumnWidth(1, wx.LIST_AUTOSIZE)
        self.list.SetColumnWidth(2, 100)

        # show how to select an item
        self.list.SetItemState(5, wx.LIST_STATE_SELECTED, wx.LIST_STATE_SELECTED)

        # show how to change the colour of a couple items
        item = self.list.GetItem(1)
        item.SetTextColour(wx.BLUE)
        self.list.SetItem(item)
        item = self.list.GetItem(4)
        item.SetTextColour(wx.RED)
        self.list.SetItem(item)

        self.currentItem = 0

    # Used by the ColumnSorterMixin, see wx/lib/mixins/listctrl.py
    def GetListCtrl(self):
        return self.list

    # Used by the ColumnSorterMixin, see wx/lib/mixins/listctrl.py
    def GetSortImages(self):
        return (self.sm_dn, self.sm_up)

    def OnRightDown(self, event):
        x = event.GetX()
        y = event.GetY()
        self.log.WriteText("x, y = %s\n" % str((x, y)))
        item, flags = self.list.HitTest((x, y))

        if item != wx.NOT_FOUND and flags & wx.LIST_HITTEST_ONITEM:
            self.list.Select(item)

        event.Skip()

    def getColumnText(self, index, col):
        item = self.list.GetItem(index, col)
        return item.GetText()

    def OnItemSelected(self, event):
        ##print(event.GetItem().GetTextColour())
        self.currentItem = event.Index
        self.log.WriteText("OnItemSelected: %s, %s, %s, %s\n" %
                           (self.currentItem,
                            self.list.GetItemText(self.currentItem),
                            self.getColumnText(self.currentItem, 1),
                            self.getColumnText(self.currentItem, 2)))

        if self.currentItem == 10:
            self.log.WriteText("OnItemSelected: Veto'd selection\n")
            #event.Veto()  # doesn't work
            # this does
            self.list.SetItemState(10, 0, wx.LIST_STATE_SELECTED)

        event.Skip()

    def OnItemDeselected(self, event):
        item = event.GetItem()
        self.log.WriteText("OnItemDeselected: %d" % event.Index)

        # Show how to reselect something we don't want deselected
        if event.Index == 11:
            wx.CallAfter(self.list.SetItemState, 11, wx.LIST_STATE_SELECTED, wx.LIST_STATE_SELECTED)

    def OnItemActivated(self, event):
        self.currentItem = event.Index
        self.log.WriteText("OnItemActivated: %s\nTopItem: %s" %
                           (self.list.GetItemText(self.currentItem), self.list.GetTopItem()))

    def OnBeginEdit(self, event):
        self.log.WriteText("OnBeginEdit")
        event.Allow()

    def OnEndEdit(self, event):
        self.log.WriteText("OnEndEdit: " + event.GetText())
        event.Allow()

    def OnItemDelete(self, event):
        self.log.WriteText("OnItemDelete\n")

    def OnColClick(self, event):
        self.log.WriteText("OnColClick: %d\n" % event.GetColumn())
        event.Skip()

    def OnColRightClick(self, event):
        item = self.list.GetColumn(event.GetColumn())
        self.log.WriteText("OnColRightClick: %d %s\n" %
                           (event.GetColumn(), (item.GetText(), item.GetAlign(),
                                                item.GetWidth(), item.GetImage())))
        if self.list.HasColumnOrderSupport():
            self.log.WriteText("OnColRightClick: column order: %d\n" %
                               self.list.GetColumnOrder(event.GetColumn()))

    def OnColBeginDrag(self, event):
        self.log.WriteText("OnColBeginDrag\n")
        ## Show how to not allow a column to be resized
        #if event.GetColumn() == 0:
        #    event.Veto()

    def OnColDragging(self, event):
        self.log.WriteText("OnColDragging\n")

    def OnColEndDrag(self, event):
        self.log.WriteText("OnColEndDrag\n")

    def OnCheckAllBoxes(self, event):
        itemcount = self.list.GetItemCount()
        [self.list.CheckItem(item=i, check=True) for i in range(itemcount)]
        self.log.WriteText("OnCheckAllBoxes\n")

    def OnUnCheckAllBoxes(self, event):
        itemcount = self.list.GetItemCount()
        [self.list.CheckItem(item=i, check=False) for i in range(itemcount)]
        self.log.WriteText("OnUnCheckAllBoxes\n")

    def OnGetItemsChecked(self, event):
        itemcount = self.list.GetItemCount()
        itemschecked = [i for i in range(itemcount) if self.list.IsItemChecked(item=i)]
        self.log.WriteText("OnGetItemsChecked: %s \n" % itemschecked)

    def OnDoubleClick(self, event):
        self.log.WriteText("OnDoubleClick item %s\n" % self.list.GetItemText(self.currentItem))
        event.Skip()

    def OnRightClick(self, event):
        self.log.WriteText("OnRightClick %s\n" % self.list.GetItemText(self.currentItem))

        # only do this part the first time so the events are only bound once
        if not hasattr(self, "popupID1"):
            self.popupID1 = wx.NewIdRef()
            self.popupID2 = wx.NewIdRef()
            self.popupID3 = wx.NewIdRef()
            self.popupID4 = wx.NewIdRef()
            self.popupID5 = wx.NewIdRef()
            self.popupID6 = wx.NewIdRef()
            self.popupID7 = wx.NewIdRef()
            self.popupID8 = wx.NewIdRef()
            self.popupID9 = wx.NewIdRef()

            self.Bind(wx.EVT_MENU, self.OnPopupOne, id=self.popupID1)
            self.Bind(wx.EVT_MENU, self.OnPopupTwo, id=self.popupID2)
            self.Bind(wx.EVT_MENU, self.OnPopupThree, id=self.popupID3)
            self.Bind(wx.EVT_MENU, self.OnPopupFour, id=self.popupID4)
            self.Bind(wx.EVT_MENU, self.OnPopupFive, id=self.popupID5)
            self.Bind(wx.EVT_MENU, self.OnPopupSix, id=self.popupID6)
            self.Bind(wx.EVT_MENU, self.OnCheckAllBoxes, id=self.popupID7)
            self.Bind(wx.EVT_MENU, self.OnUnCheckAllBoxes, id=self.popupID8)
            self.Bind(wx.EVT_MENU, self.OnGetItemsChecked, id=self.popupID9)

        # make a menu
        menu = wx.Menu()
        # add some items
        menu.Append(self.popupID1, "FindItem tests")
        menu.Append(self.popupID2, "Iterate Selected")
        menu.Append(self.popupID3, "ClearAll and repopulate")
        menu.Append(self.popupID4, "DeleteAllItems")
        menu.Append(self.popupID5, "GetItem")
        menu.Append(self.popupID6, "Edit")
        menu.Append(self.popupID7, "Check All Boxes")
        menu.Append(self.popupID8, "UnCheck All Boxes")
        menu.Append(self.popupID9, "Get Checked Items")

        # Popup the menu.  If an item is selected then its handler
        # will be called before PopupMenu returns.
        self.PopupMenu(menu)
        menu.Destroy()

    def OnPopupOne(self, event):
        self.log.WriteText("Popup one\n")
        print("FindItem:", self.list.FindItem(-1, "Roxette"))
        print("FindItemData:", self.list.FindItemData(-1, 11))

    def OnPopupTwo(self, event):
        self.log.WriteText("Selected items:\n")
        index = self.list.GetFirstSelected()

        while index != -1:
            self.log.WriteText("      %s: %s\n" % (self.list.GetItemText(index),
                                                   self.getColumnText(index, 1)))
            index = self.list.GetNextSelected(index)

    def OnPopupThree(self, event):
        self.log.WriteText("Popup three\n")
        self.list.ClearAll()
        wx.CallAfter(self.PopulateList)

    def OnPopupFour(self, event):
        self.list.DeleteAllItems()

    def OnPopupFive(self, event):
        item = self.list.GetItem(self.currentItem)
        self.log.WriteText("Text:%s, Id:%s, Data:%s" %(item.Text,
                                                       item.Id,
                                                       self.list.GetItemData(self.currentItem)))

    def OnPopupSix(self, event):
        self.list.EditLabel(self.currentItem)


#---------------------------------------------------------------------------

def runTest(frame, nb, log):
    win = TestListCtrlPanel(nb, log)
    return win

#---------------------------------------------------------------------------


overview = """\
<html>
<body>
A list control presents lists in a number of formats: list view, report view,
icon view and small icon view. In any case, elements are numbered from zero.
For all these modes (but not for virtual list controls), the items are stored
in the control and must be added to it using InsertItem method.

<p>To intercept events from a list control, use the event table macros described in
<code>wxListEvent.</code>

<h3>Mix-ins</h3>
This example demonstrates how to use mixins. The following mixins are available.

<h4>ColumnSorterMixin</h4>

<code><b>ColumnSorterMixin(numColumns)</b></code>

<p>A mixin class that handles sorting of a wxListCtrl in REPORT mode when the column
header is clicked on.

<p>There are a few requirements needed in order for this to work genericly:
<p><ol>
    <li>The combined class must have a <code>GetListCtrl</code> method that returns
    the ListCtrl to be sorted, and the list control must exist at the time the
    <code>ColumnSorterMixin.__init__()</code>method is called because it uses
    <code>GetListCtrl</code>.

    <li>Items in the list control must have a unique data value set with
    <code>list.SetItemData</code>.

    <li>The combined class must have an attribute named <code>itemDataMap</code>
    that is a dictionary mapping the data values to a sequence of objects
    representing the values in each column.  These valuesare compared in
    the column sorter to determine sort order.
</ol>

<p>Interesting methods to override are <code>GetColumnSorter</code>,
<code>GetSecondarySortValues</code>, and <code>GetSortImages</code>.

<h5>Methods</h5>
<dl>
<dt><code>SetColumnCount(newNumColumns)</code>
<dd>Informs the mixin as to the number of columns in the control. When it is
set, it also sets up an event handler for <code>EVT_LIST_COL_CLICK</code> events.

<dt><code>SortListItems(col=-1, ascending=1)</code>
<dd>Sort the list on demand.  Can also be used to set the sort column and order.

<dt><code>GetColumnWidths()</code>
<dd>Returns a list of column widths.  Can be used to help restore the current
view later.

<dt><code>GetSortImages()</code>
<dd>Returns a tuple of image list indexes the indexes in the image list for an
image to be put on the column header when sorting in descending order

<dt><code>GetColumnSorter()</code>
<dd>Returns a callable object to be used for comparing column values when sorting.

<dt><code>GetSecondarySortValues(col, key1, key2)</code>
<dd>Returns a tuple of 2 values to use for secondary sort values when the
items in the selected column match equal.  The default just returns the
item data values.

</dl>

<h4>ListCtrlAutoWidthMixin</h4>

<code><b>ListCtrlAutoWidthMixin()</b></code>

<p>A mix-in class that automatically resizes the last column to take up the
remaining width of the ListCtrl.

<p>This causes the ListCtrl to automatically take up the full width of the list,
without either a horizontal scroll bar (unless absolutely necessary) or empty
space to the right of the last column.

<p><b>NOTE:</b> This only works for report-style lists.

<p><b>WARNING:</b> If you override the <code>EVT_SIZE</code> event in your ListCtrl,
make sure you call event.Skip() to ensure that the mixin's _OnResize method is
called.

<p>This mix-in class was written by <a href='mailto:ewestra@wave.co.nz'>Erik Westra </a>

<h5>Methods</h5>
<dl>

<dt><code>resizeLastColumn(minWidth)</code>
<dd>Resize the last column appropriately. If the list's columns are too wide to
fit within the window, we use a horizontal scrollbar.  Otherwise, we expand the
right-most column to take up the remaining free space in the list. This method is
called automatically when the ListCtrl is resized; you can also call it yourself
whenever you want the last column to be resized appropriately (eg, when adding,
removing or resizing columns).  'minWidth' is the preferred minimum width for
the last column.

</dl>


<h4>ListCtrlSelectionManagerMix</h4>

<code><b>ListCtrlSelectionManagerMix()</b></code>

<p>Mixin that defines a platform independent selection policy

<p>As selection single and multi-select list return the item index or a
list of item indexes respectively.

<h5>Methods</h5>
<dl>

<dt><code>getPopupMenu()</code>
<dd>Override to implement dynamic menus (create)

<dt><code>setPopupMenu(menu)</code>
<dd>Must be set for default behaviour.

<dt><code>afterPopupMenu()</code>
<dd>Override to implement dynamic menus (destroy).

<dt><code>getSelection()</code>
<dd>Returns the current selection (or selections  as a Python list if extended
selection is enabled)


</body>
</html>
"""


if __name__ == '__main__':
    import sys,os
    import run
    run.main(['', os.path.basename(sys.argv[0])] + sys.argv[1:])

