__author__ = 'Hans-Werner Roitzsch'


from scipy import ndimage
from datetime import datetime


class LabelCounting:
	def __init__(self):
		self.label_count = 0

	def count_labels(self, mask):
		t1_get_label_count = datetime.now()
		label_im, nb_labels = ndimage.label(mask)
		t2_get_label_count = datetime.now()
		print('COUNTING OF LABELS TOOK:', TimeFunction.calculate_time_diff(t1_get_label_count, t2_get_label_count), 's', sep='')
		#print('COUNT OF LABELS:', nb_labels)

		return nb_labels