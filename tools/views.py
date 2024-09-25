from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
from .forms import ExamGenerationForm
from tools.library.utils import generator, excel_to_json
import pandas as pd
from io import BytesIO
import zipfile
import json
from module_group.models import ModuleGroup

def generate_exams_view(request):
    module_groups = ModuleGroup.objects.all()
    if request.method == 'POST':
        form = ExamGenerationForm(request.POST, request.FILES)
        if form.is_valid():
            excel_file = request.FILES['excel_file']
            number_of_exams = form.cleaned_data['number_of_exams']
            
            # Determine the file extension and specify the engine
            file_extension = excel_file.name.split('.')[-1].lower()
            if file_extension == 'xlsx':
                engine = 'openpyxl'
            elif file_extension == 'xls':
                engine = 'xlrd'
            else:
                return JsonResponse({'error': 'Unsupported file format'}, status=400)

            # Read the Excel file with the specified engine
            excel_data = pd.ExcelFile(excel_file, engine=engine)
            sheet_names = excel_data.sheet_names
            
            number_of_questions = {}
            for name in sheet_names:
                number_of_questions[name] = 20  # Adjust as needed

            generated_files = []
            for count in range(number_of_exams):
                output_file, df_combined = generator(excel_file, number_of_questions)
                json_output = excel_to_json(df_combined)

                generated_files.append((output_file, json_output, df_combined, f"Generated exam number {count + 1}:"))

            # Create ZIP file
            mem_zip = BytesIO()
            with zipfile.ZipFile(mem_zip, mode="w", compression=zipfile.ZIP_DEFLATED) as zf:
                for id, (output_file, json_output, df_combined, message) in enumerate(generated_files):
                    zf.writestr(f'exam_{id + 1}.xlsx', output_file.getvalue())
                    zf.writestr(f'exam_{id + 1}.json', json_output)
            
            mem_zip.seek(0)

            response = HttpResponse(mem_zip, content_type='application/zip')
            response['Content-Disposition'] = 'attachment; filename="exams.zip"'
            return response

    else:
        form = ExamGenerationForm()

    return render(request, 'generate_exams.html', {'form': form, 'module_groups': module_groups})
