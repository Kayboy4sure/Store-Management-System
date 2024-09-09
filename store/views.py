from django.shortcuts import render, redirect
from .models import Stock, StockHistory
from .forms import *
from django.http import HttpResponse
from django.contrib import messages
import csv


# Create your views here.
def home(request):
	form = StockSearchForm(request.POST or None)
	title = 'List of Items'
	queryset = Stock.objects.all()


	if request.method == 'POST':
		queryset = Stock.objects.filter(category__id__contains=form['category'].value(),
									item_name__icontains=form['item_name'].value(),
									last_updated__range=[form['start_date'].value(), form['end_date'].value()]
									)
		
		if form['export_to_CSV'].value() == True:
			response = HttpResponse(content_type='text/csv')
			response['Content-Disposition'] = 'attachment; filename="List of stock.csv"'
			writer = csv.writer(response)
			writer.writerow(['CATEGORY', 'ITEM NAME', 'QUANTITY'])
			instance = queryset
			for stock in instance:
				writer.writerow([stock.category, stock.item_name, stock.quantity])
			return response

	context ={
		"form": form,
		"title": title,
		"queryset": queryset,
	}

	return render(request, "index.html", context)


def add_items(request):
	form = StockCreateForm(request.POST or None)

	if form.is_valid():
		form.save()
		messages.success(request, 'Successfully Saved')
		return redirect('/')

	context = {
		"form": form,
		"title": "Add Item",
	}
	return render(request, "add_items.html", context)


def update_items(request, pk):
	queryset = Stock.objects.get(id=pk)
	form = StockUpdateForm(instance=queryset)
	if request.method == 'POST':
		form = StockUpdateForm(request.POST, instance=queryset)
		if form.is_valid():
			form.save()
			messages.success(request, 'Successfully Saved')
			return redirect('/')

	context = {
		"form":form,
		"title": "Update Item",
	}
	return render(request, 'update_items.html', context)


def delete_items(request, pk):
	queryset = Stock.objects.get(id=pk)
	if request.method == 'POST':
		queryset.delete()
		messages.success(request, 'Successfully Saved')
	return redirect('/list_items')


def store_items(request, pk):
	queryset = Stock.objects.get(id=pk)
	context = {
		"title": queryset.item_name,
		"queryset": queryset
	}
	return render(request, 'store_items.html', context)


def issue_items(request, pk):
	queryset = Stock.objects.get(id=pk)
	form = IssueForm(request.POST or None, instance=queryset)
	if form.is_valid():
		instance = form.save(commit=False)
		instance.quantity -= instance.issue_quantity
		history = StockHistory(
			id = instance.id,
			category_id = instance.category_id,
			item_name = instance.item_name,
			quantity = instance.quantity,
			issue_quantity = instance.issue_quantity,
			receive_quantity = instance.receive_quantity,
			issue_by = instance.issue_by,
			receive_by = instance.receive_by,
			last_updated = instance.last_updated,
			timestamp = instance.timestamp,
		)
		history.save()
		messages.success(request, "Issued SUCCESSFULLY. " + str(instance.quantity) + " " + str(instance.item_name) + "s now left in Store")
		instance.save()

		return redirect('/stock_items/'+ instance.id)
		# return HttpResponseRedirect(instance.get_absolute_url())

	context = {
		"title": 'Issue ' + queryset.item_name,
		"queryset": queryset,
		"form": form,
		"username": 'Issue By: ' + str(request.user),
	}
	return render(request, "add_items.html", context)


def receive_items(request, pk):
	queryset = Stock.objects.get(id=pk)
	form = ReceiveForm(request.POST or None, instance=queryset)
	if form.is_valid():
		instance = form.save(commit=False)
		instance.quantity += instance.receive_quantity
		instance.save()
		history = StockHistory(
			id = instance.id,
			category_id = instance.category_id,
			item_name = instance.item_name,
			quantity = instance.quantity,
			issue_quantity = instance.issue_quantity,
			receive_quantity = instance.receive_quantity,
			issue_by = instance.issue_by,
			receive_by = instance.receive_by,
			last_updated = instance.last_updated,
			timestamp = instance.timestamp,
		)
		history.save()
		messages.success(request, "Received SUCCESSFULLY. " + str(instance.quantity) + " " + str(instance.item_name)+"s now in Store")

		return redirect('/stock_items/'+ instance.id)

	context = {
			"title": 'Receive ' + queryset.item_name,
			"instance": queryset,
			"form": form,
			"username": 'Receive By: ' + str(request.user),
		}
	return render(request, "add_items.html", context)


def reorder_level(request, pk):
	queryset = Stock.objects.get(id=pk)
	form = ReorderLevelForm(request.POST or None, instance=queryset)
	if form.is_valid():
		instance = form.save(commit=False)
		instance.save()
		messages.success(request, "Reorder level for " + str(instance.item_name) + " is updated to " + str(instance.reorder_level))
		return redirect("/")
	context = {
			"instance": queryset,
			"form": form,
		}
	return render(request, "add_items.html", context)


def history(request):
	header = 'LIST OF ITEMS'
	queryset = StockHistory.objects.all()
	context = {
		"header": header,
		"queryset": queryset,
	}
	return render(request, "history.html",context)