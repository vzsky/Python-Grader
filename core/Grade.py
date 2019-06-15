from Problems.models import ProbsResult
import subprocess as sp
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from Grader import settings
import os
import time

def Grade(file, prob, user):
    if str(file).endswith('.c') or str(file).endswith('.cpp'):

        # Delete duplicate files
        try :
            sp.call(['rm', os.path.join(settings.MEDIA_ROOT, '{}/{}/{}_{}.cpp'.format(prob.id, user.id, user.username, prob.id))])
        except :
            pass


        path = default_storage.save('{}/{}/{}_{}.cpp'.format(prob.id, user.id, user.username, prob.id), ContentFile(file.read()))
        tmp_file = os.path.join(settings.MEDIA_ROOT, "{}/{}".format(prob.id, user.id))
        filename = "{}_{}.cpp".format(user.username, prob.id)

        # Compiling file
        Compile = ['g++', '-o', os.path.join(tmp_file, "user.sol"), '-std=c++14', os.path.join(tmp_file, filename)]
        compile_process = sp.Popen(Compile, stdin=sp.PIPE, stdout=sp.PIPE, stderr=sp.PIPE)
        compile_message = compile_process.communicate()

        sp.call(['mkdir', os.path.join(tmp_file, 'output')])

        res = []
        for i in range(1, prob.test_cases_amount+1):
            start_time = time.time()

            Run = "gtimeout 3s {}/user.sol < {}/test_case/{}/{}.in > {}/output/{}.out".format(tmp_file, settings.MEDIA_ROOT, prob.id, i, tmp_file, i)
            Run_process = sp.Popen(Run, stdin=sp.PIPE, stdout=sp.PIPE, stderr=sp.PIPE, shell=True)
            Run_message = Run_process.communicate()

            if (Run_message[1] != b''):
                res.append("X")
                continue

            print(time.time() - start_time)
            if (time.time() - start_time > 2.5) :
                res.append("T")
                continue 

            Test = "diff -w {}/test_case/{}/{}.out {}/output/{}.out".format(settings.MEDIA_ROOT, prob.id, i, tmp_file, i)
            # print(Test)
            Test_process = sp.Popen(Test, stdin=sp.PIPE, stdout=sp.PIPE, stderr=sp.PIPE, shell=True)
            Test_message = Test_process.communicate()
            if(Test_message[0] != b''):
                res.append("-")
                continue

            res.append("P")
            
        user.results.all().filter(probs=prob).delete()
        ProbsResult.objects.create(user=user, probs=prob, res=res)
        return

    raise Exception('{} is NOT a C or CPP'.format(str(file)))